# UID and GID

<!-- tl;dr starts -->

<!-- tl;dr ends -->

32-bit wide C type `uid_t` is the range of UID/GID (i.e. 0 to 4294967295).

There are 4 special UIDs:

- `0` - the `root` super-user.
- `65534` - the `nobody` user, a.k.a the "overflow" UID. Various subsystems (16-bit UIDs file systems, Network File System, user namespacing in Docker container) map unmappable users to `nobody`. The group counterpart sometimes called `nogroup` instead of `nobody`.
- `65535` - the 16-bit UID, not usable.
- `4294967295` - the 32-bit UID, not usable

Distribution range:

- `1-999`: system users. Don't map to "human" users but are used as security identities for system daemons, implement fine-grained level of privileges.
- `1000-65533` + `65536-4294967294`: regular human users.

`systemd` uses a subset of ranges:

- `60001-60513`: UIDs for home directories managed by `systemd-homed.service`
- `61184-65519`: UIDs for dynamic users.
- `524288-1879048191`: UIDs for `systemd-nspawn`'s automatic allocation of per-container UID ranges. That's why the UIDs of everything created inside Rootless Docker containers when running with a mapping between host user `1000` to container user `1000` result in `525287` in the host system.
