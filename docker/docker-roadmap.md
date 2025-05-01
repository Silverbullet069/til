# Docker Roadmap

<!-- tl;dr starts -->

Everything I learned from [Docker's roadmap.sh](https://roadmap.sh/docker) and external references.

<!-- tl;dr ends -->

## Containerized technology stack

A **container** is a lightweight, portable, isolated _software environment_ that allows engineers to package softwares with all of their dependencies and run them without experiencing behavior inconsistency across different platform. The virtualization level is **OS-level virtualization**. This environment provides isolation for the following resources: process, networking, filesystem, CPU, Memory, ...

### Linux kernel features

The containers' isolation capability comes from 2 features from **Linux kernel**: **"namespaces"** and **"cgroups"**.

1. **Linux Namespaces**

Linux Namespaces can seperate instances of global system resources, by making each container believe it has its own unique set of resources. There are several types of namespaces:

- Process ID (PID): creates distinct isolated processes
- Network (NET): allows programs to run on any ports without conflicting with other processes on the same OS that are using the same ports (hence the concept of _port mapping_)
- Mount (MNT): allows mounting and unmounting filesystems without affecting the host's filesystem
- Unix Timesharing System (UTS).
- Inter-process Communication (IPC).
- USER.

```sh
# create a virtualize system with bash shell as its sole process
sudo unshare --fork --pid --mount-proc bash

# output (fish):
root@DEVICE_NAME:/home/USER_NAME

# check processes
ps aux

# output: only 2 processes are `bash` and `ps aux`
USER         PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND
root           1  0.1  0.0 234040  7464 pts/7    S    11:39   0:00 bash
root          10  0.0  0.0 232336  4356 pts/7    R+   11:39   0:00 ps aux

# open another terminal on the system
ps aux | grep 'unshare'

# output:
root      119427  0.0  0.0 249748 14124 pts/6    S+   11:43   0:00 sudo unshare --fork --pid --mount-proc bash
root      119457  0.0  0.0 249748  5896 pts/7    Ss   11:43   0:00 sudo unshare --fork --pid --mount-proc bash
root      119458  0.0  0.0 229488  2220 pts/7    S    11:43   0:00 unshare --fork --pid --mount-proc bash
```

2. **cgroups (Control Groups)**

While namespaces provide isolation, they don't handle resource limitations. Control groups (cgroups) solve the problem of resource allocation and management. Cgroups restrict and track the amount of CPU, memory, disk I/O, and network usage that processes in a namespace can consume. This prevents containers from monopolizing host system resources and ensures fair resource distribution across multiple containers.

```sh
# create cgroup
# group type: memory (alternative: cpu, net_cls, ...)
# group name: my-process
sudo cgcreate -g memory:my-process

# directory /sys/fs/cgroup/memory/my-process is created
# inside are a bunch of files that define the memory limit for processes

ls /sys/fs/cgroup/memory/my-process
# output:
# cgroup.clone_children               memory.memsw.failcnt
# cgroup.event_control                memory.memsw.limit_in_bytes
# cgroup.procs                        memory.memsw.max_usage_in_bytes
# memory.failcnt                      memory.memsw.usage_in_bytes
# memory.force_empty                  memory.move_charge_at_immigrate
# memory.kmem.failcnt                 memory.oom_control
# memory.kmem.limit_in_bytes          memory.pressure_level
# memory.kmem.max_usage_in_bytes      memory.soft_limit_in_bytes
# memory.kmem.tcp.failcnt             memory.stat
# memory.kmem.tcp.limit_in_bytes      memory.swappiness
# memory.kmem.tcp.max_usage_in_bytes  memory.usage_in_bytes
# memory.kmem.tcp.usage_in_bytes      memory.use_hierarchy
# memory.kmem.usage_in_bytes          notify_on_release
# memory.limit_in_bytes               tasks
# memory.max_usage_in_bytes

# enforece memory limit is 50MB (base 10)
sudo echo 50000000 >  /sys/fs/cgroup/memory/my-process/memory.limit_in_bytes

# create a process with memory limit
sudo cgexec -g memory:my-process bash

# ... a lot more
```

### Container Runtimes

Namespaces and Cgroups aren't enough. **THREE** problems arised:

1. **User-friendly:** The above examples are just to show that in order to create and delete a container, you will need to run a bunch of CLI commands.

   - One to create a Linux namespace.
   - One to create a cgroup process.
   - One to define limit for cgroup process.
   - A lot more to clear namespace and cgroup.

   Also, those commands aren't supposed to be called by application engineers.

1. **User Experience while managing:** It's very, very hard to manage the containers created from cgroups and namespaces CLI tools. Think about how many terminals you will need to leave opened, how many commands with detailed arguments and options you will need to remember, ...

1. **Reusability:** People solve problems with containers by making , and later others face the same problems. How can we save them the time and effort required to replicate others' solution?

=> **Container Runtime** and **Container image** to the rescue!

Container Runtimes are container lifecycle management tool. There are a lot of container runtimes, they can be categorized into 2 types:

- **Low-level Container Runtime** (e.g. CLI tool [`runc`](https://github.com/opencontainers/runc/tree/main)):

  - Create containers with namespaces, cgroups, capabilities and filesystem access controls.
  - After the container is created, manage the container lifecycle at low-level view: Delete containers and clean up the leftovers, ...

  The features are realized using libraries such as [libcontainer](https://github.com/opencontainers/runc/blob/main/libcontainer/README.md).

- **High-level Container Runtime** (e.g. CLI tool `containerd` and `ctr`):
  - Manage container lifecycle at high-level view: Run; Stop; Pause; Delete; Monitor logs; Monitor resources; ...
  - Manage container images: List, Delete, Download container images from **container registries**; Push newly built container images onto container registries; ...

> There are many **specifications** for container runtimes: OCI (from Docker), Singularity (from Apptainer), LXC/LXD, ... **OCI** is the most popular with the highest maturity, becoming the official standard in the containerized technology community. `containerd` and `runc` supports OCI specs, that are [OCI Image Spec](https://github.com/opencontainers/image-spec), [OCI Runtime Spec](https://github.com/opencontainers/runtime-spec), ...

### Container Image and Container Registry

A **Container Image** is an executable package that includes everything required to run an application: code, configurations/settings, dependencies (programming language runtime, system tools, system libraries, ...).

A **Container Registry** is a centralized storage and distribution system for container images. They are maintained by individuals or organizations and can be used as a starting point for your containerized applications.

The most popular container registry is [Docker Hub](https://hub.docker.com/), its most well-known products are Docker Official Images, maintained by engineers from Docker Community. They are a curated set images that follow best practices, ensuring that you have access to the latest features, security updates, extensive documentation for custom configuration, ...

> **NOTE**: Some official Docker images' documentation are outdated (e.g. use depreciated options, ...).

### Filesystem for Containers

Until this point, all piece of technology we've mentioned are used to handle _isolation_, we haven't talked about _resource efficiency_ yet.

Imagine you have three Docker containers:

```
Container A: Ubuntu + Python + App1
Container B: Ubuntu + Python + App2
Container C: Ubuntu + Python + App3
```

You will need 3 complete copies of everything:

- 3 copies of Ubuntu (78.1MB x 3 = 234.3MB)
- 3 copies of Python (1.02GB x 3 = 3.06GB)
- 3 copies of App, assumed each costs 100MB = 300MB

=> Total disk usage: 3.594GB.

Computer scientists at early time have created **UnionFS**, a filesystem service which implements a union mount for other file systems. More specifically, it allows files and directories of separate file systems (now known as "branches") to be overlaid on each other like pancakes, forming a single unified view.

Here I will demonstate **OverlayFS**, a filesystem that takes after UnionFS and has been adopted into Linux kernel since version 3.18.

```sh
# Create 2 directories, one acts as read-only layer, one acts as read-write layer
mkdir readonly writable work unified

# Create 2 files on each directory
touch readonly/file{1,2}.txt writable/file{3,4}.txt

# mount them together
sudo mount -t overlay overlay -o lowerdir=readonly,upperdir=writable,workdir=work unified

# check unified content
ls unified
# output: file1.txt file2.txt file3.txt file4.txt
```

With this, files and directories from one filesystem can appear in another filesystem without creating a copy.

```sh
# modify a file1.txt inside unified/ directory
echo "I'm changing file1" > unified/file1.txt
ls -l unified
# total 4,0K
# -rw-r--r--. 1 silverbullet069 silverbullet069 19 Apr  3 23:08 file1.txt
# -rw-r--r--. 1 silverbullet069 silverbullet069  0 Apr  3 23:04 file2.txt
# -rw-r--r--. 1 silverbullet069 silverbullet069  0 Apr  3 23:23 file3.txt
# -rw-r--r--. 1 silverbullet069 silverbullet069  0 Apr  3 23:04 file4.txt

# file1.txt is copied to the writable/ directory
# the changes are made there
ls -l writable
# total 4,0K
# -rw-r--r--. 1 silverbullet069 silverbullet069 19 Apr  3 23:08 file1.txt
# -rw-r--r--. 1 silverbullet069 silverbullet069  0 Apr  3 23:04 file3.txt
# -rw-r--r--. 1 silverbullet069 silverbullet069  0 Apr  3 23:04 file4.txt

# file1.txt in readonly/ remains intact
ls -l readonly
# total 0
# -rw-r--r--. 1 silverbullet069 silverbullet069 0 Apr  3 23:04 file1.txt
# -rw-r--r--. 1 silverbullet069 silverbullet069 0 Apr  3 23:04 file2.txt
```

With this, every change is incremental change.

Container runtimes use this filesystem for container filesystem. When a container is run:

- The image layers become read-only, lower layers.
- A new writable layer is created for the container.
- All layers are combined to create the container's filesystem.

### Container Management Platform

However, there are still a few remaining problems for containerized stack to reach full maturity: calling high-level container runtimes is still a hassle, building container images, providing GUI to work with containers, ...

We need a dedicated platform that integrates all container runtimes under a unified framework and exposes an intuitive interface that's sufficiently abstracted, allowing engineers to focus entirely on deploying their applications without needing to understand the underlying infrastructure.

## Docker

**Docker**, is the most popular container management platform. **Docker Engine**, the software behind the magic, acts as a client-server application with the following components:

- A CLI client `docker`. It provides a unified interface to interact with all of the following components:
  - Low-level container runtime.
  - High-level container runtime.
  - Two plugins: **Docker Buildx** (or Docker Build) to build container images and **Docker Compose** to operate on multiple containers at once.
- A server, or a daemon `dockerd`. This daemon called to high-level container runtime `docker-containerd` (similar to `containerd`) via socket/API. High-level container runtime `docker-containerd` calls to low-level container runtime `docker-runc` (similar to `runc`).
- APIs which acts as interfaces that programs can use to talk to and instruct the daemon `dockerd`. This API allows CLI client `docker`, Unix sockets `/var/run/docker.sock`, Docker SDK, Portainer, ... to talk to daemon `dockerd`.

> There is an application called [Docker Desktop](https://www.docker.com/products/docker-desktop/) which provides GUI to do operations on containers. But personally, CLI is more than enough for me.
>
> **NOTE:** Standalone Docker Engine is only available in Linux.

This is the hierarchy:

```
Docker Desktop (GUI)
  └── Docker Engine (complete container platform)
      └── dockerd (Docker daemon)
          └── docker-containerd (high-level container runtime)
              └── docker-runc (low-level container runtime)
                  └── libcontainer (low-level container runtime library)
                      └── Linux kernel features (namespaces, cgroups, etc.)
```

### Data Persistence

By default, the storage within a Docker container is _ephemeral_, meaning any creation, modification and deletion made inside a container will only persist until the container is removed. Once removed, all changes are lost.

Docker containers are designed to be _stateless_. Statelessness enables fast and consistent deployment of applications across different environments.

However, it poses a great challenges when you want to persist the data, especially when you want everything stay the same after you restart the container or recreate the container from an updated version of the container image.

Docker introduces **Volume Mounts** and **Bind Mounts**, the technology behinds critical features: **Persistency** - data stay even when containers are removed and **Data sharing** - multiple containers can share the same volume.

#### Volume Mounts

_Pros and practices:_

- **Not easy to access from host**: volumes are managed by Docker, stored in Docker's storage directory: `/var/lib/docker/volumes/`.
- **Security**: can be more safely shared among multiple containers, unlike bind mounts who have host system as intermediary.
- **Platform-independent**: works on both Linux and Windows container (nobody use Windows container by the way).
- **High-performace I/O**: managed entirely by Docker, thus optimized.
- **Pre-populating newly created volume**: new volumes can have their content pre-populated by a container or build.
- **Easy to migrate and backup**.

_Mounting a volume over existing data:_

- If a non-empty volume is mounted into a directory in the container, in which files and directories exists, the pre-existing files are obscured (not lost!).
- If an empty volume is mounted into a directory in the container, in which files and directories exists, the pre-existing files are copied into the volume (by default). Use `volume-nocopy` in `--mount` option to prevent this behavior.

_Named and anonymous volume:_

- Anonymous volumes are volumes without a name, but still given a uniquely identifiable ID within the host system.
- Anonymous volumes are persisted even after containers are removed, **unless** a `--rm` flag is used when creating the container.
- Multiple containers creation will results in multiple anonymous volumes creation.
- Anonymous volumes aren't shared by default, they must be explicitly mounted using their ID (which is AFTER the container has been run).

_Use cases:_

- **Database persistence**: Storing database files (like MySQL, PostgreSQL, MongoDB) so data persists across container restarts or replacements.
- **Application data**: Maintaining application state, user-generated content, or configuration settings that need to persist.
- **Shared content**: Sharing data between multiple containers that need access to the same files (like multiple web servers accessing the same content).
- **Log storage**: Centralizing log files from containers to ensure they aren't lost when containers are removed, making them accessible for monitoring tools.
- **Cache storage**: Persisting application cache data across container restarts to improve performance.

```sh
# -v option can automatically create volume if it hasn't been created first
# however, the same doesn't apply for --mount option
docker volume create demo-log-data

docker run --name=demo-volume --rm -d -p 80:80 -v demo-log-data:/logs docker/welcome-to-docker
# or
docker run --name=demo-volume --rm -d -p 80:80 --mount type=volume,src=demo-log-data,dst=/logs docker/welcome-to-docker

docker exec -it demo-volume /bin/sh
echo "abcdefghijklkmn" > /logs/test.txt

sudo du -h $(docker volume inspect demo-log-data | jq -r .[].Mountpoint)
```

#### Bind Mounts

_Pros and practices:_

- **Easy to access from host**: unlike volume mounts that are managed by Docker, it's easy to access files and directories from the host.
- **Security**: bind mounts have **write** access to mounted files and directories on the host by default. Use `readonly` for `--mount` option or `:ro` for `--volume` option to prevent the container from writing to the mount.
- **Platform-dependent**: bind mounts rely on the host machine's filesystem having a specific directory structure available, resulting in more caveats when migrating.
- **Performance**: relies on host filesystem.

_Files ownership_:

If you have configured `docker` running with root privileges (check by running `docker info | grep -i "rootless"`), all operations on the container side are done as root, e.g. running `whoami` outputs `root`. Newly created files have `root` ownership, even on the host system side.

There are ways to get around this, one of them is specifying the user ID when running the container:

```sh
docker run --name=demo-volume --rm -p 80:80 -u 1000:1000 --mount type=bind,src=./logs,dst=/logs docker/welcome-to-docker
```

However, most of the time this will fail since a container needs to run instructions defined in its container image, and if there is at least one instruction requiring `root` privileges, the running process will be terminated. Check the logs (by omitting the `-d` option) to determine if this situation has occurred.

_Configure the SELinux label:_

If your OS use SELinux (like my Fedora KDe 41), adding `:z` or `:Z` value in `--volume` option can modify the SELinux label of the host file or directory being mounted into the container:

- `:z` - bind mount content is shared among multiple containers.
- `:Z` - bind mount content is private and unshared.

It's not possible to modify the SELinux label using `--mount` option.

> **NOTE**: Use with extreme cautions. Its effect can spread outside the scope of Docker. Bind-mounting a system directory (i.e. `/home`, `/usr`, ...) with `Z` option renders the host system inoperable.

_Use cases:_

1. Sharing source code/build artifacts between a development environment on the Docker host and a container. You can code in one place, and reflect the state in another place, just like when I'm developing my dad's website.

1. Creating/Generating files in a container and persist the files onto the host's filesystem. Application settings that you've spent hours to tweak are saved.

1. Sharing configuration files from the host machine to containers. Docker provides DNS resolution to containers by default, by mounting `/etc/resolv.conf` from host machine into each container.

```sh
mkdir logs
docker run --name=demo-volume --rm -d -p 80:80 --mount type=bind,src=./logs,dst=/logs docker/welcome-to-docker

docker exec -it demo-volume /bin/sh
echo "abcdefghi" > test.txt

ls -l logs
# output:
# -rw-r--r--. 1 root            root            10 Apr  4 11:19 test.txt
```

### Containerized Database

```sh
# run a local containerized database
# -v option persist database data
docker run \
  --rm \
  -d \
  --name=demo-mysql \
  -u $(id -u):$(id -g) \
  -p 3307:3306 \
  --network demo-network \
  -e MYSQL_ROOT_PASSWORD=my-secret-pw \
  -e MYSQL_DATABASE=mydb \
  -v demo-mysql-volume:/var/lib/mysql \
  mysql:latest

# Access the shell of a containerized database
docker exec -it demo-mysql mysql -u root -p
# or
docker exec -it demo-mysql bash
mysql -u root -p

# Connect to a containerized database from host system
mysql -h 127.0.0.1 -P 3307 -u root -p # my-secret-pw

# Connect to a containerized database from another container
# with --network option
docker run \
  --rm \
  -d \
  --name=demo-phpmyadmin \
  -p 8080:80 \
  -e PMA_HOST=demo-mysql \
  -e PMA_PORT=3306 \
  --network=demo-network \
  phpmyadmin:latest
```

Use Docker Compose to run a database

`Dockerfile`:

```sh
# syntax=docker/dockerfile:1

# use the base image mysql:latest
FROM mysql:latest

# set environment variable (this can also be set in Docker Compose file)
ENV MYSQL_DATABASE=mydb

# copy custom scripts or configuration files from host to the container
COPY ./scripts/ /docker-entrypoint-initdb.d/
```

`docker-compose.yml`:

```yml
services:
  db:
    image: mysql:latest
    environment:
      MYSQL_ROOT_PASSWORD: my-secret-pw
      MYSQL_DATABASE: mydb
    volumes:
      - my-db-volume:/var/lib/mysql
      #-/path/to/my/datadir:/var/lib/mysql

  phpmyadmin:
    image: phpmyadmin:latest
    environment:
      PMA_HOST: db
      PMA_PORT: 3306
    ports:
      - 8080:80
    depends_on:
      - db

volumes:
  my-db-volume:
```

According to [the documentation on Official Docker Image for MySQL on DockerHub](https://hub.docker.com/_/mysql), files with extension `.sh`, `.sql` and `.sql.gz` that are found in `/docker-entrypoint-initdb.d` will be executed in alphabetical order. By doing so, it's easy to mount a SQL dump into that directory and build a custom image with pre-populated data.

`./scripts/customers.sql`

```sql
-- Cre: https://www.mysqltutorial.org/mysql-basics/mysql-uuid/
CREATE TABLE IF NOT EXISTS mydb.customers (
  id BINARY(16) DEFAULT (UUID_TO_BIN(UUID())) PRIMARY KEY,
  name VARCHAR(255)
);

INSERT INTO mydb.customers(id, name)
VALUES(UUID_TO_BIN(UUID()),'John Doe'),
      (UUID_TO_BIN(UUID()),'Will Smith'),
      (UUID_TO_BIN(UUID()),'Mary Jane');
```

Run Docker Compose:

```
docker compose up
```

**MySQL configuration file:** Can be specified in the following place:

- `/etc/mysql/my.cnf`
- `/etc/mysql/conf.d/my.cnf` (recommended)
- `/etc/mysql/mysql.conf.d/my.cnf`

Persist the settings with bind mounts.

**Configuration with a `cnf` file:** Use `docker run` behavior - anything specified after the image name are commands and options for `cmd` in image.

```sh
# change the default encoding and collation for all tables to use utf-8
docker run --name demo-mysql -e MYSQL_ROOT_PASSWORD=my-secret-pw -d mysql:latest --character-set-server=utf8mb4 --collation-server=utf8mb4_unicode_ci
```

**Environment variables:**

- `MYSQL_ROOT_PASSWORD`: mandatory, specify the password that will be set for `root` superuser account.
- `MYSQL_DATABASE`: optional, create a new database on image startup.
- `MYSQL_USER`, `MYSQL_PASSWORD`: optional, create a new user. This use will be granted superuser permissions (`GRANT ALL`) for the database specfied by `MYSQL_DATABASE`.
- `MYSQL_RANDOM_ROOT_PASSWORD`: optional, set to a non-empty value (e.g. `yes`) will generate random initial password for the root user using `openssl` and print it to stdout.
- `MYSQL_ONETIME_PASSWORD`: optional, force password change for `root` account after first login.

These environment variables can be referred in `docker exec` command.

**Docker secrets:** A list of custom environment variables with `_FILE` suffix whose value is the path to the file IN THE CONTAINER that contains the sensitive information

```sh
docker run --name demo-mysql -e MYSQL_ROOT_PASSWORD_FILE=/run/secrets/mysql-root -d mysql:latest
```

**Data persistent:** Either volume mounts or bind mounts. Consider the pros and cons of each solution.

**No connection until MySQL init completes**: Setup a connect-retry loop before the MySQL service starts.

**Running as an arbitrary user**: `-u 1000:1000` option.

**Create database dumps and restore data from dump files:**

```sh
docker exec demo-mysql sh -c 'exec mysqldump --all-databases -uroot -p"$MYSQL_ROOT_PASSWORD"' > /some/path/on/your/host/all-database.sql

# -i = leave stdin open, so data can be populated
docker exec -i demo-mysql sh -c 'exec mysql -uroot -p"$MYSQL_ROOT_PASSWORD"' < /some/path/on/your/host/all-database.sql
```

### Building Container Images

To build a container image, engineers need to write **Dockerfile** - a text document that contains a list of instructions used by Docker Engine (its plugin, Docker Buildx, to be precise) to build an image.

Container images are built up as a stack of **layers**. A layer is a set of filesystem changes - additions, modifications, deletions - that represents the result of a specific instruction in a Dockerfile. In short, any instruction _that modifies the filesystem_ creates a new layer. Each layer contains only the differences from the layer before it.

When you're pulling a single image from a container registry, you're actually downloading muliple layers. If you calculate the sum of the size of all layers, it's equal to the size of the image.]

Container images layers are designed to be _reused_ extensively:

- Layers can be shared between different images.
- When pushing or pulling images, Docker checks for existing layers on host filesystem and transferred only new or modified layers.

#### Layer components

1. Content files: The actual files and directories that were added, modified, or deleted.
1. Metadata: information about the layer (id, content hash, size, creation timestamp, instruction, ...). You can examine a layer by running `docker image history IMAGE_NAME`.
1. A pointer to its parent layer: Except for the base layer, each layer references the layer below it (remember, this is a stack).

#### Behind-the-scene of the container execution

1. After each layer is downloaded, it's extracted into its own directory on the host filesystem.
2. When a container runs from an image, a union filesystem stacks these layers to create a unified view.
3. Any changes made to a running container are written to a writable container layer.

```Dockerfile
# syntax=docker/dockerfile:1
FROM mysql:latest                             # Base layer - ALL layers from mysql:latest image
ENV MYSQL_DATABASE=mydb                       # Layer 1 - setting environment variable
COPY ./scripts/ /docker-entrypoint-initdb.d/  # Layer 2 - initial scripts
```

```sh
docker image history my-custom-mysql

# output
# IMAGE          CREATED        CREATED BY                                      SIZE      COMMENT
# 7e2437ba8a44   5 hours ago    COPY ./scripts/ /docker-entrypoint-initdb.d/…   147B      buildkit.dockerfile.v0
# <missing>      5 hours ago    ENV MYSQL_DATABASE=mydb                         0B        buildkit.dockerfile.v0
# <missing>      2 months ago   CMD ["mysqld"]                                  0B        buildkit.dockerfile.v0
# <missing>      2 months ago   EXPOSE map[3306/tcp:{} 33060/tcp:{}]            0B        buildkit.dockerfile.v0
# <missing>      2 months ago   ENTRYPOINT ["docker-entrypoint.sh"]             0B        buildkit.dockerfile.v0
# <missing>      2 months ago   COPY docker-entrypoint.sh /usr/local/bin/ # …   13.8kB    buildkit.dockerfile.v0
# <missing>      2 months ago   VOLUME [/var/lib/mysql]                         0B        buildkit.dockerfile.v0
# <missing>      2 months ago   RUN /bin/sh -c set -eux;  microdnf install -…   522MB     buildkit.dockerfile.v0
# <missing>      2 months ago   ENV MYSQL_SHELL_VERSION=9.2.0-1.el9             0B        buildkit.dockerfile.v0
# <missing>      2 months ago   RUN /bin/sh -c set -eu;  {   echo '[mysql-to…   226B      buildkit.dockerfile.v0
# <missing>      2 months ago   RUN /bin/sh -c set -eux;  microdnf install -…   142MB     buildkit.dockerfile.v0
# <missing>      2 months ago   RUN /bin/sh -c set -eu;  {   echo '[mysqlinn…   246B      buildkit.dockerfile.v0
# <missing>      2 months ago   ENV MYSQL_VERSION=9.2.0-1.el9                   0B        buildkit.dockerfile.v0
# <missing>      2 months ago   ENV MYSQL_MAJOR=innovation                      0B        buildkit.dockerfile.v0
# <missing>      2 months ago   RUN /bin/sh -c set -eux;  key='BCA4 3417 C3B…   3.17kB    buildkit.dockerfile.v0
# <missing>      2 months ago   RUN /bin/sh -c set -eux;  microdnf install -…   16.7MB    buildkit.dockerfile.v0
# <missing>      2 months ago   RUN /bin/sh -c set -eux;  arch="$(uname -m)"…   2.36MB    buildkit.dockerfile.v0
# <missing>      2 months ago   ENV GOSU_VERSION=1.17                           0B        buildkit.dockerfile.v0
# <missing>      2 months ago   RUN /bin/sh -c set -eux;  groupadd --system …   2.77kB    buildkit.dockerfile.v0
# <missing>      2 months ago   CMD ["/bin/bash"]                               0B        buildkit.dockerfile.v0
# <missing>      2 months ago   ADD oraclelinux-9-slim-amd64-rootfs.tar.xz /…   113MB     buildkit.dockerfile.v0
```

### Image Building Best Practices

There are **ELEVEN** best practices for image building.

#### 1. Use multi-stage builds

_Definition:_ Use multiple `FROM` statements in a Dockerfile. Each `FROM` instruction can use a different base image, and each begins a new stage of the build.

By selectively copying artifacts from one stage to another and leaving behind unnecessary components, you can achieve **FOUR** key benefits:

- **Separation of concerns**: Dockerfile is more organized, easy to maintain.
- **Reduce image size**: final stage ALWAYS exclude unnecessary build tools.
- **Better security**: less tools, less files => less attack surface.
- **Cache utilization**: more reusable stages => less cache invalidation.

```Dockerfile
# syntax=docker/dockerfile:1

# name your stages
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

# --from=0 is the first `FROM` instruction
#COPY --from=0 /bin/hello /bin/hello
# better approach: --from=name
COPY --from=build /bin/hello /bin/hello
# external image as a stage
# by doing so, you always have the most up-to-date configuration file
#COPY --from=nginx:latest /etc/nginx/nginx.conf /nginx.conf
CMD ["/bin/hello"]
```

> **NOTE:** Only transfer binaries without external dependencies. I've tried to copy `/bin/echo` from `alpine:latest` to `scratch` and `/bin/echo` can't be run from `scratch`.

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

Code written in compiled programming languages (C, C++, Go, Rust) can be compiled in one stage and then the compiled binaries can be copied into a smaller runtime image.

Code written in interpreted languages (JS, TS, Ruby, ...) can be built and minified in one stage using build tools (Vite, Webpack, Next.js Compiler, etc.) and then the final files can be copied into a smaller runtime image.

#### 2. Stop at a target build stage

Sometimes you don't need the output of the final stage, maybe you need the output of the first stage, second stage, ...

Usually engineers make each stage reflects the environment that it's gonna be deployed:

- `build` stage => engineers do manual debugging.
- `debug` stage => debug using debug tools.
- `testing` stage => automation testing tool + synthetic test data
- `production` stage => real data + strip off unused files.

```sh
docker build --target build -t hello-build .
```

#### 3. Pick up a previous stage where it left off

```Dockerfile
# syntax=docker/dockerfile:1

FROM alpine:latest AS builder
RUN apk --no-cache add build-base

FROM builder AS build1
COPY source1.cpp source.cpp
RUN g++ -o /binary source.cpp

FROM builder as build2
COPY source2.cpp source.cpp
RUN g++ -o /binary source.cpp
```

#### 4. Reducing Image Size

**Avoid unnecessary files.** For example, when building images derived from Debian/Ubuntu-based Docker images that use `apt` package manager:

- When running `apt-get update` command, `apt` downloads package lists from repositories to `/var/lib/apt/lists/`, these files are only needed during the package installation process.
- After the packages have been installed with `apt-get install`, those package lists are no longer needed for the running container.

```Dockerfile
# ...
RUN apt-get update && apt-get install -y extra-runtime-dependencies && rm -rf /var/lib/apt/lists/*
# for Official Debian/Ubuntu images, apt-get clean is run automatically
# ...

```

Reviews your `COPY`, `RUN` and `ADD` instructions. If you spot unnecessary files and directories, write a `.dockerignore` file to exclude all of them. It has the same syntax as `.gitignore`.

Q: Why don't people just install then remove instantly?
A: Whenever a layer is created, it's stored in cache. Even if users remove unnecessary files and directories in subsequent layers, they still exist in the previous layers.

#### 5. Combining command

You can minimize the number of layers by combining commands using `&&`.

#### 6. Choose the right base image and right use cases

Right "base":

- Docker Official Images.
- Docker Verified Publisher.
- Docker-Sponsored Open Source.

Right "use cases": 1 for building, 1 for testing, 1 for production.

#### 7. Create ephemeral containers

Containers that are easy to be stopped and destroyed, rebuilt and replaced with minimum configuration

#### 8. Decouple applications

Don't try to put 2 or more applications into a single image, only put 1 application per image.

#### 9. Sort multi-line arguments

Avoid duplication of packages, easier to maintain.

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

#### 10. Automating the building and testing process

When there is a change in version control, use a CI/CD platform (e.g. GitHub Actions) to update (build, tag your Docker image and test it).

#### 11. Maintain dependency on base image

For images that require the latest version of their base image, you must bypass the cache entirely:

```sh
docker build --no-cache ...
```

Docker caches the results of each instruction. Caches reduces build time and minimizing bandwidth usage. To minimize cache miss, you must understand when cache invalidation triggers:

- Changes to files copied with COPY or ADD instructions.
- Changes to RUN instructions.

=> The layers that're the results of those instructions will be invalidated and the same applied to all subsequent layers.

For applications that required maximum reliability, refrain using `:latest` tag. Instead, pin base image version by specifying `@[digest]` tag.

=> Downside: requires maintainer to lookup the digest value tediously, also opting out of automated security patches.

=> Recommendation: enforce version pinning at **major and minor version** (e.g. `FROM alpine:3.20`) or use Docker Scout's Remediation (at this point of writing, it's still in Beta). It can warn and prompt user to update when there is a new version.

### Image Tagging Best Practices

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

### Docker Compose

_Secrets:_ Instead of writing your **API_KEY=**, your password into `docker run` command or `environment:` attribute in Docker Compose file, these sensitive information should be written using Docker Secrets.

### DockerHub and GitHub Container Registry

I like this because it plays nicely with GitHub Actions.

## References

- [Roadmap.sh's "Roadmap: Docker"](https://roadmap.sh/docker)
- [2022-11-14, Quân Huỳnh, Linux Namespaces và Cgroups: Container được xây dựng từ gì?](https://devopsvn.tech/devops/linux-namespaces-va-cgroups-container-duoc-xay-dung-tu-gi#block-39ed33ffb7a641bda46566016460bbe2)
- [2022-11-14, Quân Huỳnh, Tìm hiểu sâu hơn về Container - Container Runtime là gì?](https://devopsvn.tech/devops/tim-hieu-sau-hon-ve-container-container-runtime-la-gi)
- [Wikipedia, Docker (software)](https://en.wikipedia.org/wiki/Docker_%28software%29)
- [Wikipedia, UnionFS](https://en.wikipedia.org/wiki/UnionFS)
- [Docker Docs "Persisting container data"](https://docs.docker.com/get-started/docker-concepts/running-containers/persisting-container-data/)
- [Docker Docs "Use containerized databases"](https://docs.docker.com/guides/databases/)
- [Docker Docs "Understanding image layers"](https://docs.docker.com/get-started/docker-concepts/building-images/understanding-image-layers/#explanation)
- [Docker Docs "Multi-stage builds"](https://docs.docker.com/build/building/multi-stage/)
- [Docker Docs "Building best practices"](https://docs.docker.com/build/building/best-practices/)
- [Docker Docs "Docker build cache"](https://docs.docker.com/build/cache/)
- [Docker Hub "MySQL"](https://hub.docker.com/_/mysql)
- [GitHub Docs "Introduction to GitHub Packages"](https://docs.github.com/en/packages/learn-github-packages/introduction-to-github-packages)
- [nirmalkushwah08's "Docker Image Tagging Strategy"](https://medium.com/@nirmalkushwah08/docker-image-tagging-strategy-4aa886fb4fcc)
