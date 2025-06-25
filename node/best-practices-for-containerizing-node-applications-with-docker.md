# Best Practices For Containerizing Node Applications With Docker

<!-- tl;dr starts -->

In order to create production-ready files for [huveco-static](https://github.com/Silverbullet069/huveco-static), I need to use some build tools. Luckily I found some decent Node packages. Again, to not pollute your system environment, containerize it. But containerize it how?

<!-- tl;dr ends -->

## Cheatsheet

`.dockerignore`:

```dockerignore
.dockerignore
node_modules
npm-debug.log
Dockerfile
.git
.gitignore
.npmrc
```

`Dockerfile`:

```Dockerfile
# build
FROM node:latest AS build
RUN apt-get update && apt-get install -y --no-install-recommends dumb-init
WORKDIR /usr/src/app
COPY package*.json /usr/src/app/
# npm v10.9.2
RUN --mount=type=secret,mode=0644,id=npmrc,target=/usr/src/app/.npmrc npm ci --include=prod

# production
FROM node:20.9.0-bullseye-slim
ENV NODE_ENV=production
COPY --from=build /usr/bin/dumb-init /usr/bin/dumb-init
USER node
WORKDIR /usr/src/app
COPY --chown=node:node --from=build /usr/src/app/node_modules /usr/src/app/node_modules
COPY --chown=node:node . /usr/src/app
ENTRYPOINT ["/usr/bin/dumb-init", "--"]
CMD ["node", "server.js"]
```

CLI:

```sh
docker build . -t production:latest --secret id=npmrc,src=.npmrc
```

Another `Dockerfile` that prevent cache invalidation when bumping versions:

```Dockerfile
ARG ALPINE_VERSION=3.11
ARG NODE_VERSION=22.14.0

##########################
# Cache-preserving image #
##########################

FROM alpine:${ALPINE_VERSION} AS deps

# prevent leftover cache files from polluting image layer
RUN apk --no-cache add jq

# prevent cache invalidation from changes in fields other than dependencies

COPY package.json .
COPY package-lock.json .

# override the current package version (arbitrarily set to 1.0.0) so it doesn't invalidate the build cache later

RUN (jq '{ dependencies, devDependencies }') < package.json > deps.json
RUN (jq '.version = "1.0.0"' | jq '.packages."".version = "1.0.0"') < package-lock.json > deps-lock.json

#################
# Builder image #
#################

FROM node:${NODE_VERSION} AS builder

WORKDIR /usr/src

COPY --from=deps deps.json ./package.json
COPY --from=deps deps-lock.json ./package-lock.json
# npm v10.9.2
# no cache invalidation here
RUN npm ci --include=prod

COPY public/ public/
COPY src/ src/
COPY webpack/ webpack/
# restore original file
COPY package.json .

ENV NODE_ENV=production

RUN npm run build

####################
# Production image #
####################

FROM node:${NODE_VERSION}-alpine${ALPINE_VERSION}

WORKDIR /usr/src

RUN chown node:node /usr/src && \
    apk add --no-cache dumb-init

COPY --chown=node:node .env.example .

COPY --from=builder --chown=node:node /usr/src/dist/ dist/
# use original file
COPY --from=builder --chown=node:node /usr/src/package.json .

ENV PORT=80
ENV NODE_ENV=production

USER node

CMD ["dumb-init", "node", "dist/server"]
```

## References

- [Liran Tal, Yoni Goldberg, Snyk Blog "10 best practices to containerize Node.js web applications with Docker"](https://snyk.io/blog/10-best-practices-to-containerize-nodejs-web-applications-with-docker/)
- [abstractvector's " Lightweight node.js Dockerfile "](https://gist.github.com/abstractvector/ed3f892ec0114e28b3d6dcdc4c39b1f2)

<!-- TODO: read https://snyk.io/blog/ten-npm-security-best-practices/ -->
