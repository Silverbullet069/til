# Avoid External File With `dockerfile_inline:`

<!-- tl;dr starts -->

I want to build an ultimate `docker-compose.yml` file that can deploy all services with a click of an button from anywhere with the least dependency, including external file.

<!-- tl;dr ends -->

Here is when I want to add SSH client and change the directory ownership of `/var/run/tailscale` where it will put a UNIX `.sock` file

```yml
service:
  tailscale:
    # ...
    build:
      context: .
      dockerfile_inline: |
        FROM tailscale/tailscale:latest
        RUN apk add --no-cache openssh
        RUN mkdir -p /var/lib/tailscale && chmod 1000:1000 /var/run/tailscale
    # ...
```
