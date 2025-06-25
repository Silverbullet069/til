# Use Docker Run To Create A Simple Sandbox

<!-- tl;dr starts -->

Sometimes, when I want to use a FOSS application but somewhat unpopular with very few users and high no. of dependencies that I can't conduct code auditing, I create a simple sandbox using Rootless Docker + `docker run [OPTIONS]` command to create a very restricted Docker container.

<!-- tl;dr ends -->

## Cheatsheet

```sh
#!/bin/sh

# NOTE: if you're running Rootless Docker, the host ownership is very different
# E.g. If you run the service using -u 1000:1000, host ownership refers to 525287:525287
docker run \
  --name="image_name" \
  --init \
  --rm \
  --user="$(id -u):$(id -g)" \
  --read-only  \
  --network none \
  --security-opt=no-new-privileges:true \
  --volume="${PWD}:/app" \
  --workdir="/app" \
  # an alpine-based iamge
  silverbullet069/image_name:latest \
  "$@"
```
