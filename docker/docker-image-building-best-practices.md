# Docker Image Building Best Practices

<!-- tl;dr starts -->

How to build Docker images for multiple environments with maximum performance and tightest security?

<!-- tl;dr ends -->

## General knowledge

### Dockerfile frontend parser

When building images using Docker, BuildKit loads a frontend to parse your Dockerfile. This frontend can came:

- Internally from your container images. I bet most Docker Official Images have one embedded
- Externally by specifying `syntax` directive, pointing to the specific image (yeah the frontend came from an image)
  ```Dockerfile
  # syntax=docker/dockerfile:1      # MOST RECOMMENDED, updated with the latest 1.x.x minor and patch release.
  # syntax=docker/dockerfile:1.2    # updated with the latest 1.2.x patch release, stops when 1.3.0 roll out.
  # syntax=docker/dockerfile:1.2.1  # immutable, never updated
  # syntax=docker.io/docker/dockerfile:1
  # syntax=example.com/user/repo:tag@sha256:abcdef...
  ```

Using custom Dockerfile, you will get:

- Use the latest features and get auto bug fixes without updating Docker daemon.
- Enforce Dockerfile frontend consistency between users.
- Try out new features before they are integrated in Docker daemon.
- (Advanced) Build your own Dockerfile frontend with custom features

Personally, I don't need it. All of my images are derived from base images with high maturity and often get updated.

### Cache Invalidation

When you're building the same Docker image multiple times, you will need to know how to optimize the build cache in order to make the builds run fast.

```sh
# syntax=docker/dockerfile:1
FROM ubuntu:latest

RUN apt-get update && apt-get install -y build-essentials
COPY main.c Makefile /src/
WORKDIR /src/
RUN make build
```

Each instruction translates to a layer in final image. Image layers are like a stack, with each layer adding more content on top of the layers that came before it.

```txt
+------------------------------+
| FROM ubuntu:latest           |  <-- Base image layer
+------------------------------+
| RUN apt-get update &&        |  <-- Installs build-essentials
| apt-get install -y           |
| build-essentials             |
+------------------------------+
| COPY main.c Makefile /src/   |  <-- Copies files into image
+------------------------------+
| WORKDIR /src/                |  <-- Sets working directory to /src/
+------------------------------+
| RUN make build               |  <-- Runs 'make build' in /src/
+------------------------------+
```

Whenever a layer changes, that layer will need to be re-built.

> E.g. if `main.c` and/or `Makefile` are changed, the `COPY` instruction will have to run again in order for those changes to appear in the image (or "invalidate" the cache for this layer).

If a layer changes, **all other layers that come AFTER it have their cache invalidated as well**.

```
+------------------------------+
| FROM ubuntu:latest           |  ✓
+------------------------------+
| RUN apt-get update &&        |  ✓
| apt-get install -y           |
| build-essentials             |
+------------------------------+
| COPY main.c Makefile /src/   |  ✕
+------------------------------+
| WORKDIR /src/                |  ✕
+------------------------------+
| RUN make build               |  ✕
+------------------------------+
```

The instructions correspond to these layers have to be rerun, cost subsequent builds precious time.

### Which instructions cause Cache Invaliation?

For the `ADD`, `COPY` and `RUN --mount=type=bind` instructions, the builder calculates checksum from file metadata to determine whether cache is valid. Cache is invalidated if the file metadata has changed for any of the files involved

> **NOTE:** time modification doesn't affect metadata checksum.

Cache checking doesn't look at the changes of files' content to determine a cache match.

> `RUN apt-get update -y` instruction use command string itself to find a match, that's why you can easily get outdated files from `apt` in subsequent builds since it's always a cache hit.

> `RUN apk add curl` shares the same fate.

To force a re-execution of the `RUN` instruction and cause cache invalidation, you can:

- Make sure a layer before it has changed
- Clear the build cache ahead of the build using `docker builder prune`
- Use `docker build --no-cache` or `--no-cache-filter`, the latter option lets you specify a specific build stage to invalidate the cache.

For `RUN --mount-type-secret,id=TOKEN,env=TOKEN` instruction, build secrets aren't part of the build cache. Therefore build secrets changes doesn't result in cache invalidation. To force cache invaliation, use `docker build --build-arg CACHEBUST=1`

## FOURTEEN Best Practices for building Docker images

These best practices are sorted from easiest to hardest.

### 1. Write `.dockerignore` files

Exclude files that didn't want to be included in the build context. It uses glob patterns similar to `.gitignore`:

- `.git`: you don't need version control history in build context, unless you want to run Git commands in build steps.
- Directories containing _build artifacts_, such as _binaries_. For non-production build stages, they are redundant, for production build stage, they are replaced.
- _Vendor directories for package managers_, such as `node_modules`.
- Pretty much similar in content to `.gitignroe`.

### 2. Use 3rd-party images from trusted source

These THREE image sources are widely known for their high standard in building images:

- Docker Official Images.
- Docker Verified Publisher.
- Docker-Sponsored Open Source.

### 3. Create ephemeral containers

Containers that are easy to be stopped, destroyed, rebuilt and replaced with minimum configuration.

### 4. Decouple applications

Don't try to put more than ONE application into a single image.

### 5. Use CI/CD platform to automate the building and testing process

When there is a change in version control, use a CI/CD platform (e.g. GitHub Actions) to update (build, tag your Docker image and test it).

### 6. Optimize tooling for production

Some frameworks or libraries may only turn on the optimized configuration that is suited to production if the environment variable that indicates the deployed environment is set to `production`.

However, most frameworks or libraries automatically set this environment variable to `production` when built with build tools.

#### Examples

```Dockerfile
FROM node ...
ENV NODE_ENV=production
```

- [Express](https://expressjs.com/en/advanced/best-practice-performance.html#set-node_env-to-production)

### 7. DO NOT run containers as root

> **NOTE:** if you're building a development environment, running as `root` is fine. It solves the problem of not being able to write into bind mounts when the container is running as non-root.

#### Problem

Threat assessment: if an attacker is able to compromise the web application in a way that allows for [Command Injection](https://www.snyk.io/blog/command-injection/) or [Directory Path Traversal](https://www.snyk.io/blog/snyking-in-directory-traversal-vulnerability-exploit-in-the-st-package/), these will be invoked with the user who owns the application process. If that process happens to be root, then they can do **virtually everything** within the container, including [attempting a container escape](https://www.snyk.io/blog/a-serious-security-flaw-in-runc-can-result-in-root-privilege-escalation-in-docker-and-kubernetes/) or [privilege escalation](https://www.snyk.io/blog/kernel-privilege-escalation/).

#### Solution

There is an old security principle that dates back to the early days of Unix: **The principle of least privilege**.

Now, there is a new saying: "Friends don't let friends run containers as root!"

By default, most (if not all) of the Docker Official Images don't specify a `USER` directive. The ownership of files and directories that have been populated while building the image will be `root`, and the ownership of the processes created after running container is also `root`:

```sh
docker run --rm -u "$(id -u):$(id -g)" alpine sh -c "ls -la /"

# drwxr-xr-x   19 root     root             0 Apr 20 14:08 .
# -rwxr-xr-x    1 root     root             0 Apr 20 14:08 .dockerenv
# drwxr-xr-x    2 root     root           858 Feb 13 23:04 bin
# drwxr-xr-x    5 root     root           340 Apr 20 14:08 dev
# drwxr-xr-x   17 root     root            56 Apr 20 14:08 etc
# drwxr-xr-x    2 root     root             0 Feb 13 23:04 home
# drwxr-xr-x    6 root     root           146 Feb 13 23:04 lib
# drwxr-xr-x    5 root     root            28 Feb 13 23:04 media
# drwxr-xr-x    2 root     root             0 Feb 13 23:04 mnt
# drwxr-xr-x    2 root     root             0 Feb 13 23:04 opt
# dr-xr-xr-x  613 nobody   nobody           0 Apr 20 14:08 proc
# drwx------    2 root     root             0 Feb 13 23:04 root
# drwxr-xr-x    3 root     root             8 Feb 13 23:04 run
# drwxr-xr-x    2 root     root           790 Feb 13 23:04 sbin
# drwxr-xr-x    2 root     root             0 Feb 13 23:04 srv
# dr-xr-xr-x   13 nobody   nobody           0 Apr  8 05:37 sys
# drwxrwxrwt    2 root     root             0 Feb 13 23:04 tmp
# drwxr-xr-x    7 root     root            40 Feb 13 23:04 usr
# drwxr-xr-x   11 root     root            86 Feb 13 23:04 var

docker run --rm alpine ps x
# PID   USER     TIME  COMMAND
#     1 root      0:00 ps x

docker run --rm alpine id
# uid=0(root) gid=0(root) groups=0(root),1(bin),2(daemon),3(sys),4(adm),6(disk),10(wheel),11(floppy),20(dialout),26(tape),27(video)
```

Some (not all) Docker Official Images support changing process and newly created files/directories ownership when running container via passing user ID and group ID from host system:

- Docker `run` command: `docker run -u $(id -u):$(id -g)` (usually `1000:1000`)
- Docker Compose file: `user: "${UID}:${GID}"` attribute with `UID` and `GID` specified as [1 out of 6 solution inside this blog](https://blog.giovannidemizio.eu/2021/05/24/how-to-set-user-and-group-in-docker-compose/).

The behavior from now on will be:

- Every process within the container run as user ID 1000 and group ID 1000.
- Every new file or directory created will be owned by user ID 1000 and group ID 1000.

```sh
docker run --rm -u "$(id -u):$(id -g)" alpine id
# uid=1000 gid=1000 groups=1000

docker run --rm -u "$(id -u):$(id -g)" alpine ps x
# PID   USER     TIME  COMMAND
#     1 1000      0:00 ps x
```

> **NOTE:** Not all Docker Official Images practice the principle of least privileges, especially network-based application such as web servers because they need `root` privileges to run network operations.

Node Docker Official Image default image as well as its varients, include a least-privilleged user of the same name: `node`.

When using it as the base image, writing `USER node` instruction makes sure every process run, every files and directories created **AFTER** that instruction is owned by the `node` user. However, the same didn't apply for the processes, files and directories **BEFORE** that. They are still owned by `root` and that's how Docker works by default.

Remember to use `COPY --chown=node:node` instruction to copy resources and set ownership to copied files as `node` and double-check instructions run before `USER node` since they will be run as `root`.

#### Examples

```Dockerfile
COPY --chown=node:node . /usr/src/app
# ...
USER node
```

### 8. Use explicit and deterministic tag for base images

#### Problem

Some people often use default or `:latest` tag

```Dockerfile
# tag not found => :latest tag is used
FROM node
# tag :latest
FROM node:latest
```

1. Introduce inconsistency, or non-deterministic in subsequent Docker image builds - subsequent build after a while might pull a newly built Docker image.

2. Default or `:latest` tag isn't always the tag that's appropriated for your use case. Most default images (e.g. Node, phpMyAdmin, ...) are based on a full-fledged OS, full of libs and tools that you may not need to run your application. Bigger images result in:
   - More download size => More storage requirement. More time to download and rebuild the image
   - More softwares => More potential vulnerability vectors (supply chain attack, ...).

#### Solution

Using lock files, deterministic installation can be realized in `npm` (`package-lock.json`, `npm ci`) and `pip`(`requirements-lock.txt`) package managers.

For Docker image builds, the same can be done by using more specific tags.

1. Use small Docker images. Some images provide a `:slim` tag with smaller software footprint on the Docker image.

   > For [Node](https://hub.docker.com/_/node/) image, an **up-to-date, Debian-based, slim distribution + a LTS Node.js runtime version** is the ideal choice.
   >
   > Until 2025-04-20, this tag is ideal: `FROM node:22.14.0-bookworm-slim` ([URL](https://github.com/nodejs/docker-node/blob/f6908ff3eb35a5d0c8fc60086fd29ae16e3abdba/23/bookworm-slim/Dockerfile))
   >
   > IMO: They even have a tag `lts-slim` that corresponds to the above tag, but I think it's still unpredictable.
   >
   > Note that, some images provide a `:alpine` tag. It does contain smaller software footprint but it substantially differs in other traits. That makes it a non-optimal production base image.

2. Use Docker image digest.

   E.g.

   - `SHA256` hash: `FROM node@sha256:1c18d9ab3af4585870b92e4dbc5cac5a0dc77dd13df1a5905cea89fc720eb05b`
   - Tag + `SHA256` hash: `FROM node:22.14.0-bookworm-slim@sha256:1c18d9ab3af4585870b92e4dbc5cac5a0dc77dd13df1a5905cea89fc720eb05b`

   Using the Docker image digest ensures the most deterministic image build, BUT it could be confusing or counterproductive for some image scanning tools, who may not know how to interpret this. Use **Solution #1** if this occurs to you.

#### Q: Which images should we use with their default (`:latest` tag)?

The ones that are tightly controlled. Anything that needs to be put inside them is reviewed thoroughly. They're unlikely to cause inconsistency even when their version gets bumped.

These images are also widely known for their slimness. Using these images as base images will tremendously reduce the size of the final image:

I know only **TWO** such images: [Alpine](https://hub.docker.com/_/alpine) and [Scratch](https://hub.docker.com/_/scratch):

- **Alpine:** 6-7MB in size, provides all of the GNU/Linux's OS utilities, ignore `git`, `bash`, ...
- **Scratch:** provides nothing at all, but useful for creating images that only host statically linked binaries.

```Dockerfile
FROM alpine:latest
# ...

FROM scratch:latest
# ...
```

> **NOTE:** Dynamic linked binaries use dynamic linked libraries from OS environment, therefore these binaries can't be moved outside of their environment. Unlike them, static linked binaries bundle everything they need inside their executable files, they can run everywhere they want, even in `scratch` image.

### 9. Safely terminate the process running the application

Key concerns that engineers need to remember:

- An orchestration engine, such as Docker Swarm, Kubernetes, Docker Engine itself, needs a way to send signals to the process in the container. They are mostly signals to terminate an application: `SIGTERM`, `SIGKILL`.

- The application process may run indirectly, and if that happens then it's not always guaranteed that it will receive these signals.

- The Linux kernel treats processes that run as Process ID 1 (or PID 1) differently than any other process ID.

Now, **the 1st problem** is the following command is **indirectly** running the Node application by **directly** invoking the `npm` client:

```Dockerfile
CMD "npm" "start"
```

Sadly, the `npm` CLI doesn't forward ALL events to the node runtime. So this is a bad practice!

=> **Solution for the 1st problem:** invoke the `node` CLI directly against a file called `server.js`.

Next, **the 2nd problem** is there are two ways to specify the `CMD` directive:

- **The shellform notation:** The container spawns a shell interpreter that wraps the process. In such cases, the shell may not properly forward signals to the process.

```Dockerfile
CMD "node" "server.js"
```

- **The execform notation:** The container spawns a process without wrapping it in a shell. Any signals sent to the container are directly sent to the process. It's specified using JSON array notation.

```Dockerfile
CMD ["node", "server.js"]
```

=> **Solution to the 2nd problem** is to use the execform notation

However, this `node` process run as `PID 1`, **this is the 3rd problem**. Every `PID 1` process takes some of the responsibilities of an init system, which is typically responsible for initializing an OS system and its processes. The kernel also treats `PID 1` process differently: the handling of a `SIGTERM` signal to a running `PID 1` process won't invoke a default fallback behavior of killing the process if the process doesn't already set a handler for it.

In short, no more graceful process termination by default.

=> **Solution to the 3rd problem:** Use a simple process supervisor and init system designed to run as PID 1 inside minimal container environments. The process immediately spawns your command (`node`) as its child process, handles signal forwarding, cleans up zombie process.

1. When running via `docker run`, use `--init true` option. Docker then uses [`krallin/tini`](https://github.com/krallin/tini) underneath.

   ```sh
   docker run --init true ...
   ```

1. When running via `docker-compose.yml`, specify `init:true` directive. This also uses `tini`.

   ```yml
   # ...
   init: true
   # ...
   ```

1. When building a new image using Dockerfile, consider nstalling [Yelp/dumb-init](https://github.com/Yelp/dumb-init), which is a tool made by Yelp engineers. `dumb-init` is statically linked and has a small software footprint.

   ```Dockerfile
   RUN apt-get update && apt-get install -y --no-install-recommends dumb-init
   CMD ["dumb-init", "node", "server.js"]

   # or even better
   COPY --from=build /usr/bin/dumb-init /usr/bin/dumb-init
   ENTRYPOINT ["/usr/bin/dumb-init", "--"]
   CMD ["node", "server.js"]
   ```

> **NOTE:** `docker kill` and `docker stop` commands only send signals to the container process with `PID 1`. If a Node application is run from a shell script, take notes that shell instance, such as `/bin/sh`, will not forward signals to child processes. Your app will never get a `SIGTERM`. Very similar to invoking `node` application using `shellform`, but much worse.
>
> **NOTE:** when bind mounting a folder in the host system to container, even if you match host system's user ID with container's user ID, the ownership and permissions of the directory doesn't stay originally.

### 10. Find and fix security vulnerabilities

Using Snyk CLI, you can test the container for any security issues: the number of OS dependencies (including runtime), known vulnerabilities of the runtime and the other softwares within the container.

```sh
npm install -g snyk
snyk auth
snyk container test node:22.14.0-bookworm-slim --file=Dockerfile
```

There are 5 ways to fix Docker image vulnerabilities:

- Rebuild the Docker image: depends on the upstream Docker base image that you will receive the patch updates or not.

  > With Node Docker Official Image, the team may be slower to respond with image updates. Rebuilding the Docker image will not be very effective.

- Explicitly install OS system updates for packages, including security patches

  ```Dockerfile
  RUN apt-get update -y && apt-get upgrade -y
  ```

- Ad-hoc tnteract with Snyk CLI. It will show the number of vulnerabilities, the severity and the source of each vulnerability, then recommend other newer version base images to switch to with fewer critical vulnerabilities in specific, vulnerabilities in general.

- Use Snyk CLI in CI automation. The CLI is very flexible, it can be applied to any workflow, even [GitHub Actions](https://www.snyk.io/blog/see-snyk-and-github-in-action-at-github-universe/).

- Import Docker images hosted in a registry (Docker Hub, Github Container Registry, ...) into Snyk. The platform will find vulnerabilities in them and prorduce advices in the Snyk UI as well as monitoring the imported Docker images on an ongoing basis for dewly discovered security vulnerabilities.

### 11. Reduce image size by reviewing the instructions carefully

More specifically, reviews your `COPY`, `RUN` and `ADD` instructions.

1. Rearrange them, layers that's made using the above instructions are prone to change and should be put on bottom.

2. Reduce unnecessary image layers from multiple `RUN` instructions by combining them into 1 `RUN` instruction using `&&` operator. Remember to sort multi-line arguments, this practice avoids package duplication, easier to maintain and peer-reviewed.

E.g. When building images derived from Debian/Ubuntu-based images that use `apt` package manager:

- When running `apt-get update` command, `apt-get` downloads package lists from repositories to `/var/lib/apt/lists/`, these files are only needed during the package installation process.
- After the packages have been installed with `apt-get install`, those package lists are no longer needed for the running container, therefore run `rm -rf /var/lib/apt/lists/*`.
- What about `apt-get clean` ? For Debian/Ubuntu-based Docker Official Image, `apt-get clean` is run automatically.

```Dockerfile
# Cre: https://github.com/docker-library/buildpack-deps
RUN apt-get update && apt-get install -y --no-install-recommends \
  bzr \
  cvs \
  git \
  mercurial \
  subversion \
  && rm -rf /var/lib/apt/lists/*
```

```Dockerfile
RUN apt-get update && apt-get install -y extra-runtime-dependencies && rm -rf /var/lib/apt/lists/*
```

```Dockerfile
# Cre: https://stackoverflow.com/a/40944512/9122512
RUN apk --no-cache add bash
```

> **NOTE:** `apt-get` is used in these situation instead of `apt` because `apt` is used in user interaction situation, and `apt-get` is used in automatic running situation.

**Q:** Why is it bad practice to use one `RUN` instruction to install and a separate `RUN` instruction to remove files?

**A:** Whenever a layer is created, it is stored in the cache. Even if users remove unnecessary files and directories in subsequent layers, they still exist in the previous layers. This is why creating and removing files that contain sensitive information must happened in the same `RUN` instruction.

3. If you spot unnecessary files and directories and can't explicitly excluded them, write a `.dockerignore` file.

4. Fetch remote files in build rather than bundling the files into build context using `COPY --from=IMAGE_NAME:latest/PATH/TO/FILE` or `ADD` command

5. Avoid unnecessary resources for all stages, that includes dev, test, build, production.

E.g. for Node images, use `RUN npm ci --only=production` to install only packages in `dependencies` from `package-lock.json`.

When building production images:

- Code written in compiled programming languages (C, C++, Go, Rust, ...) can be compiled statically in one stage. The binaries can be copied into a smaller runtime image, such as `scratch`.
- Modern web applications made from frameworks and libraries, which often include various build tools, can have their production-ready resources generated by these tools.

### 12. Multi-stage builds

A Dockerfile should specify multiple build stages, each stage starts with a dedicated `FROM` instruction.

_Pros and practices:_

1.  **Decluttering**: Tools from different environments are no longer intertwined in a single build stage.
1.  **Prevent information leak:** hide sensitive information inside `build` image and copy the resources downloaded using that information into the `production` image.

    ```Dockerfile
    ## build
    FROM node:latest AS build # latest is okay, maybe you need `gcc` to compile native `npm` package
    RUN apt-get update && apt-get install -y --no-install-recommends dumb-init
    ARG NPM_TOKEN
    WORKDIR /usr/src/app
    COPY package*.json /usr/src/app/
    RUN echo "//registry.npmjs.org/:_authToken=$NPM_TOKEN" > .npmrc && \
      npm ci --only=production && \
      rm -f .npmrc
    # or even better
    RUN --mount-type=secret,mode=0644, id=npmrc,target=/usr/src/app/.npmrc npm ci --only=production
    # then run docker build . -t nodejs-tutorial --secret id=npmrc,src=.npmrc
    # remember to put .npmrc into .dockerignore

    ## production
    FROM node:22.14.0-bookworm-slim
    ENV NODE_ENV=production
    COPY --from=build /usr/bin/dumb-init /usr/bin/dumb-init
    USER node
    WORKDIR /usr/src/app
    COPY --chown=node:node --from=build /usr/src/app/node_modules /usr/src/app/node_modules # copy the resources downloaded from the sensitive information
    COPY --chown=node:node . /usr/src/app
    CMD ["dumb-init", "node", "server.js"]
    ```

1.  **Stop at a specific build stage**: Sometimes you don't need the output of the production stage, maybe you the development stage, test stage, ...

    - `base` stage => prepare dependencies from `package.json`, `package-lock.json` for subsequent builds without triggering cache invalidation.
    - `testing` stage => automation testing tool + synthetic test data
    - `build` stage => prepare the final resources for `production` stage
    - `production` stage => copy from `build` stage.

1.  **Parallelism:** Build stages can run in parallel i.e. all build stages for different environments (dev, test, staged, ... , production) can be built at the same time.
1.  **Less attack surface**: less tools, less files => less attack surface.
1.  **Cache utilization**: more reusable stages => less cache invalidation.

Subsequent build stages can reuse the following existing artifacts:

- Remote images (duh, of course).
- Prior build stages.

  ```Dockerfile
  FROM foo AS bar
  # ...
  FROM baz
  ```

- Resources from prior build stages

  ```Dockerfile
  FROM foo AS bar
  # ...
  FROM baz
  COPY --from=bar
  # COPY --from=0     # referred using integer, if bar is the 1st build stage
  ```

- Resources from remote images, doing so will ensure you have the most up-to-date configuration file
  ```Dockerfile
  FROM foo AS bar
  # ...
  FROM --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
  ```

#### Example

```Dockerfile
# syntax=docker/dockerfile:1

FROM golang:latest AS build
WORKDIR /app
COPY <<EOF ./main.go
package main

import "fmt"

func main() {
  fmt.Println("hello, world")
}
EOF
RUN go build -o /bin/hello ./main.go

# the most lightweight container image
FROM scratch
#COPY --from=0 /bin/hello /bin/hello
COPY --from=build /bin/hello /bin/hello
CMD ["/bin/hello"]
```

Test run:

```sh
docker build -t hello .
docker images hello
# output
# hello       latest      56fe838a1a1b   19 seconds ago   2.2MB

docker image history hello
# IMAGE          CREATED         CREATED BY                              SIZE      COMMENT
# 56fe838a1a1b   4 minutes ago   CMD ["/bin/hello"]                      0B        buildkit.dockerfile.v0
# <missing>      4 minutes ago   COPY /bin/hello /bin/hello # buildkit   2.2MB     buildkit.dockerfile.v0
```

### 13. Hot Reloading

#### Problem

Even though layer caching can speed up the image build process, we still don't want to rebuild the container image with Every. Single. Code. Change.

#### Solution

Use bind mounts and hot reloading utilities from the tool inside container.

#### Examples

React application with Vite as frontend build tool:

```yml
volumes:
  - type: bind
    source: ../05-example-web-application/client-react/
    target: /usr/src/app/
  - type: volume
    target: /usr/src/app/node_modules
```

Node application with `nodemon`:

```sh
# add `nodemon` to `devDependencies` in `package.json` and also update `package-lock.json` without installing anything
npm install --package-lock-only --save-dev nodemon
```

```Dockerfile
## base
# slim - image that contains the minimal packages needed to run `node`
# use when only the `node` image will be deployed
FROM node:slim AS base
WORKDIR /usr/src/app
COPY package*.json ./

## dev
FROM base AS dev
# cache files and directories between build stages
RUN --mount=type=cache, target=/usr/src/app/.npm \
  npm set cache /usr/src/app/.npm && \
  npm install
COPY . .
# "npm run dev" corresponds to nodemon src/index.js
CMD ["npm", "run", "dev"]

## production
FROM base AS production
ENV NODE_ENV=production
# reuse the cache from dev build stage
RUN --mount=type=cache, target=/usr/src/app/.npm \
  npm set cache /usr/src/app/.npm && \
  # npm ci - clean install of `npm` product for automated environment
  npm ci --only=production
USER node
COPY --chown=node:node ./src/ .
EXPOSE 3000
CMD ["node", "index.js"]
```

### 14. Maintain dependency on base image

If you need to rebuild images that require the latest version of their base image, their `apt-get update -y`, `apt add curl`, you have to force cache invalidation:

```sh
docker build [--no-cache] [--no-cache-filter=BUILD_STAGE_NAME]
```

For applications that required maximum reliability, refrain using `:latest` tag. Instead, pin base image version by specifying `@[digest]` tag.

=> Downside: requires maintainer to lookup the digest value tediously, also opting out of automated security patches.

=> Recommendation: enforce version pinning at **major and minor version** (e.g. `FROM alpine:3.20`) or use Docker Scout's Remediation (at this point of writing, it's still in Beta). It can warn and prompt user to update when there is a new version.

## Image Tagging Best Practices

- Release new version through CI/CD ? Automation tagging.
- Different environments => Different tags.
- If you create 1 Git tag per release, use that Git tag as Docker image tag.
  E.g. Git tag `v1.2.3` => Tag `:1.2.3`.
- If you follow a branching strategy for software development, branch names can be used to manage Docker image tags.
  E.g. `git checkout -b release/1.2.3` => Tag `:1.2.3`.
- If you host unstable release, use date-based tags for Docker images.
  E.g. if release date is _2023-06-30_ and it's version `.1.2.3` now => tag `1.2.3-20230630`.
- If you host stable release, use `:latest` tag, this allows you to easily refer to the latest version without specifying the exact version number.
  > However, some say you should avoid the ambiguous `:latest` tag in production.
- If each Git commit is a release, use Git commit hash.
  E.g. `1.2.3-f8c4aa1`

_Consistency_ and _clariry_ are essential to avoid confusion, and ensure smooth version control of Docker images.

Be that as it may, you must choose a tagging strategy that aligns with your team's workflow and requirements.

## Dockerfile instructions

### ADD and COPY

`COPY`: copy files from _build context_ or a stage in multi-stage build using `--from=` option.
`ADD`:

- Fetch files from remote HTTPS or Git URLs.
- Better than `wget` or `curl`
- Checksum validation
- Support parsing branches, tags and subdirectories.

> **NOTE:** don't use `ADD` for files that will be deleted later.

Sometimes you just want to temporately copy files from _build context_ to your image without persistency, use bind mount instead of `COPY`. It's considered to be more efficient that `COPY`:

```Dockerfile
RUN --mount=type=bind,source=requirements.txt,target=/tmp/requirements.txt \
    pip install --requirement /tmp/requirements.txt
```

### LABEL

Help organize images by project, record license info, aid in automation, ...

### RUN

```Dockerfile
# non exec form (default)
# /bin/sh -c is used

# > docker image history ubuntu
# IMAGE          CREATED       CREATED BY                                      SIZE      COMMENT
# b1d9df8ab815   6 weeks ago   /bin/sh -c #(nop)  CMD ["/bin/bash"]            0B
# ...

# exec form
# explicitly choose shell
RUN ["OTHER_SHELL", "param1", "param2"]

# /bin/sh -c interpreter evaluates exit code of the last operation in the pipe to determine success
# if `wget` failed yet `wc -l` succeed, the build step succeed
RUN wget -O - https://example.com | wc -l > /number
# if `wget` failed regardless `wc -l` succeed or not, the build step failed
RUN set -o pipefail && wget -O - https://example.com | wc -l > /number

# split long line using \ or heredoc
# always run `apt-get-update` and `apt-get install -y --no-install-recommends` together using &&
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
      package-bar \
      package-baz \
      package-foo=x.x.* \
    && rm -rf /var/lib/apt/lists/*
    # cre: https://ubuntu.com/blog/we-reduced-our-docker-images-by-60-with-no-install-recommends


# Official Debian/Ubuntu-based image automatically run `apt-get-clean`
#RUN apt-get clean

# Cache Busting - prevent using cache layers
# Install latest package versions, with version pinning, without manual intervention.
RUN --no-cache ...

# Hot reloading
RUN --mount=type=bind ...
RUN --mount=type=cache ...
```

- Similarity: Both aren't included in the final iamge
- Differences:

<!-- prettier-ignore -->
| Feature | `type=bind` | `type=cache` |
| --- | --- | --- |
| Purpose | Accessing existing files | Speed up repeated operations, reduce network bandwidth |
| Persistence between build stages | No | Yes |
| Default mode | Read-only | Read-write |
| Source | Build context (set of files that your build can access), or other stages | New empty directory |
| Common use | Access build artifacts, config files, ... |  Package managers, build tools |

### CMD

- Run the software contained in image, along with arguments
- Should always be run in _exec_ form: `CMD ["executable", "param1", "param2"]`
- Most cases, in _exec_ form, `CMD` should be given an interactive shell so when users run `docker run -it [IMAGE]` they can get dropped into a usable shell.

```Dockerfile
CMD ["perl", "-de0"]
CMD ["python"]
CMD ["php", "-a"]
```

- Other rare cases, `CMD` _exec_ form, specifying parameters only when used in conjection with `ENTRYPOINT`.

```Dockerfile
CMD ["param1", "param2"]
```

### EXPOSE

- Use common, traditional port for application.
- Can be overriden if users execute `docker run -p` option.

### ENV

- Configure execution environment for builds specific to services in container.
- Update `PATH` environment variable. Still I would like to use absolute path all the time.
- Set commonly used version numbers.

- This is different from `ARG` or `LABEL`:

  - `ARG` isn't persist in the final image build, only used during build time, not recommended for passing secrets.
  - `LABEL` is for metadata (versioning, description, maintainer)

- Set and unset environment variable must stay on the same `RUN` instruction, since each instruction creates an immutable layer that can't be changed even in future layer.

### [ENTRYPOINT](https://docs.docker.com/reference/dockerfile/#entrypoint)

Set the image's main command, `CMD` only specifies default flags (argument and options)

Used in combination with a helper script if the starting process requires more than 1 step.

### [VOLUME](https://docs.docker.com/reference/dockerfile/#volume)

Expose database storage, configuration storage, files and folders created by Docker containers.

_Q: What is the benefits of specifying `VOLUME` instruction in `Dockerfile` when user can create whatever volumes that want?_
A: It creates anonymous volume, fully managed by Docker. It's also a form of docs indicating users that certain files and directories are intended for persistency.

You can't mount a host directory from within the Dockerfile since host directory meant to be available during container run-time and not during build.

### USER

By default, all Docker container are run using root privillege. To ensure or services that can be run without privileges:

```Dockerfile
# Create user and group:
RUN groupadd -r postgres && useradd --no-log-init -r -g postgres postgres

# Use new user name and user group for the remainder of the current stage
USER postgres:postgres
```

Avoid using `sudo`. If you have to initialize daemon as `root`, but running it as non-root, use [tianon/gosu](https://github.com/tianon/gosu)

Avoid switching `USER` back and forth to reduce layers and complexity.

### WORKDIR

Always use absolute paths for `WORKDIR`.

Avoid using proliferating instructions such as `RUN cd ... && do-something`. Hard to read, troubleshoot and maintain.

### ONBUILD

Only used when you're using multiple `Dockerfile`.

## Reference

- [Docker Docs's "Multi-stage Build"](https://docs.docker.com/build/building/multi-stage/)
- [Docker Docs's "Docker build cache"](https://docs.docker.com/build/cache/)
- [Docker Docs's "Optimize for building in the cloud"](https://docs.docker.com/build-cloud/optimization/)
- [Docker: Beginner to Pro's "Hot Reloading"](https://courses.devopsdirective.com/docker-beginner-to-pro/lessons/11-development-workflow/01-hot-reloading)
- [Liran Tal, Yoni Golberg, "10 best practices to containerize Node.js web applications with Docker"](https://snyk.io/blog/10-best-practices-to-containerize-nodejs-web-applications-with-docker/)
