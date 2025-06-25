# Rootless Docker Enable IPv6 Support

<!-- tl;dr starts -->

I've spent hours trying to understand why I can't ping to `google.com` to its IPv6 address. It's because Rootless Docker networking is very restricted when compared to Rootful Docker.

<!-- tl;dr ends -->

By reading [moby/moby#48257](https://github.com/moby/moby/issues/48257), I've found that Rootless Docker use a user-mode networking tool called `slirp4netns` to provide network connectivity to network namespaces without requiring root privileges. You can say `slirp4netns` is a default networking backend for Rootless Docker.

How it works:

- It creates a virtual NIC inside the container's isolated network namespace (try running `docker exec --rm alpine:latest ip addr show`)
- It then acts as a user-space router and NAT gateway for traffic originating from this isolated network namespace.
- More specifically, it emulates the network connection for the containers, forwarding their traffic to the host's network, and vice-versa (from host's network to container's network).
- It provides a basic DHCP service to assign IP addresses to containers within the isolated network namespace.

Cons:

- Higher latency, lower throughput compared to kernal-space networking inside a traditional Rootful Docker set up.
- Immature IPv6 support.
- Limited ICMP support.
- Port forwarding high complexity.

Its IPv6 support in general is too inferior to its alternative toolkit, `passt` (Pass The Address, STupidly) and its CLI tool `pasta`. I can run `ping6` with `pasta` but not `slirp4netns`.

How to switch from `slirp4netns` to `pasta`:

```sh
$ mkdir -pv ~/.config/systemd/user/docker.service.d
$ touch ~/.config/systemd/user/docker.service.d/override.conf
$ cat << EOF > ~/.config/systemd/user/docker.service.d/override.conf
[Service]
Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_FLAGS=--ipv6"
Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_NET=pasta"
Environment="DOCKERD_ROOTLESS_ROOTLESSKIT_PORT_DRIVER=implicit"
EOF
$ systemctl --user restart docker
```
