# Fix error `ZONE_CONFLICT: 'docker0' already bound to a zone` when restarting Docker

<!-- tl;dr starts -->

IMO, I didn't even know the origin of this bug, I just know how to fix it.

<!-- tl;dr ends -->

It's so frustrating to go to `journalctl -xeu docker.service` (or `journalctl --user -xeu docker.service` if you're running Rootless Docker) to identify it's the same problem again and again:

```
... ZONE_CONFLICT: 'docker0' already bound to a zone ...
```

Thanks to [reytech-dev/Fix.md](https://gist.github.com/reytech-dev/1cbbb158df374018be454537de32a428), here is the solution:

```sh
# check if docker zone exists in one of your zones
$ firewall-cmd --get-active-zones
# if "docker" zone is available (duh)

# non-persistently change interface to docker0
$ sudo firewall-cmd --zone=docker --change-interface=docker0
# persistedly change interface to docker0
$ sudo firewall-cmd --permanent --zone=docker --change-interface=docker0
$ sudo systemctl restart firewalld

# (optional) check again if docker0 leaves the existing zone or not
$ firewall-cmd --get-active-zones
```
