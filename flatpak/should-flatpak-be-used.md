# Should Flatpak be used?

<!-- tl;dr starts -->

Seeing numerous posts on Reddit, unresolved GitHub Issues about different aspects of Flatpak's security, I'm a little disappointed. There isn't an official announcement to tackle these problems after all those years. Therefore I'm going to stop idolizing Flatpak sandbox capability.

<!-- tl;dr ends -->

## TL;DR

Using Flatpak application, although it's immature, is still better than not using at all. Flatpak is and always will be a "partial sandbox". Best practice is to **review all existing permissions and make necessary tweaks**.

If you need maximum security, especially when running cracked games or investigating malware behavior, a "closed sandbox" like a virtual machine is much better. Starting from May 2024, VMware Workstation Pro will be free for personal use, so this approach is worth considering.

Of course, if Flatpak is the only choice, or the native built provided by package managers bloats system environment (e.g. having to install GTK-based applications into KDE-based OS), or suffers from GUI problems, one must used Flatpak.

## Flatpak sandbox mechanism

First of all, Flatpak framework installed Flatpak apps' libraries and dependencies, known as **runtimes**. Flatpak framework (not Flatpak application) does use OS libs but it's

> Unlike `firejail` who's wrapped around apps using the ones came from OS, a successful attack against `firejail` can wreak havoc inside OS.

Flatpak used [containers/bubblewrap](https://github.com/containers/bubblewrap), its goal is to run app in a sandbox, where it restricted access to system resources using a set of permissions. Bubblewrap's design avoid allowing privilege escalation by turning off setuid binaries.

> Applications that are Bubblewrap-ed uses more memory than running native build. Weighes the options between a secure application that

> Modern Linux distros have security measures to prevent privileges escalation as well. I've been unsuccessfully in replicating a privilege escalation scenario inside my Fedora KDE system.

Without permissions mismanagement, a successful attack against Flatpak sandbox would need to exploit 2 vulnerabilities: one in the application, and one in the sandbox itself ([MikeNovember, 2024-10-21](https://forums.linuxmint.com/viewtopic.php?p=2540726#p2540726)).

## Permission models

There are two ways of granting permissions:

### Static permission

_Blacklisting all, whitelist some_, means that Flatpak starts with no filesystem access from the host, and then via CLI command `flatpak override --filesystem=`, KDE's Flatpak Permissions or [Flatseal](https://github.com/tchx84/Flatseal), access to sysroot or user directories are granted explicitly.

### Dynamic permission

To ensure application's stability, along with provide flexibility in granting permissions that are applied with users' use cases, Flatpak brings out _portal_, or _file chooser_, an interface between the Flatpak sandbox and the system that can leverage user interaction to implicitly grant read/write access to files/directories.

Keep in mind that file chooser provides read/write access as a normal user, it can not have superuser rights so it can not access sysroot.

> Q: Portals can override existing static permissions, how to not using portals at all?
>
> A:
>
> - [BillDietrich in flatpak/flatpak#3977](https://github.com/flatpak/flatpak/issues/3977) stated that portals are non-standard, blackboxing. Portals can override static permissions set outside the app. For novice users, this can act as a sandbox escape if they don't know what they're doing. He said that the static permissions should be the ultimate permissions. There is no possible method to disable this feature both locally per-application or globally according to [Arxcis's comment on flatpak/flatpak#3977](https://github.com/flatpak/flatpak/issues/3977#issuecomment-733162395).
> - [alexlarsson's comment on flatpak/flatpak#3977](https://github.com/flatpak/flatpak/issues/3977#issuecomment-748906741) said Flatpak wasn't designed to let user turn portals off, there is still no progress in controlling the file chooser.

## Different types of permissions

### Basic Permissions

- Internet connection

  - This is what makes Flatpak more superior than Linux's users and groups since user-based GUI apps need stricter resource control than system-based apps because of the enormous number of resources they share.

  - X-Server listening for TCP can be exploited to gain control over display, abstracting DBus or X11 sockets, ...

  - However, [Flatpak Docs "Sandbox Permissions Footnote #2"](https://docs.flatpak.org/en/latest/sandbox-permissions.html#f2) stated that network access also grants access to all host services listening on abstract Unix sockets, which affects X Server and the session bus which listens to abstract Unix sockets by default. [rusty-snake's comment on netblue30/firejail#4685]() also mentioned about "private netns not possible (without custom wrapper scripts)".

> This can be solved if Flatpak application can disable network connection entirely but the apps that need sandboxing the most are apps required Internet connection. Quite the paradox.

- Pulseaudio sound server.

> Flatpak proposed the use of: 1. Wayland Compositor to isolate monitor, 2. PipeWire to isolate sound.

- Device access: if disabled, only insignificant ones like `/dev/null` are used [Flatpak Docs "Sandbox Permissions > Device access"](https://docs.flatpak.org/en/latest/sandbox-permissions.html#device-access).

### Filesystem Access ([Flatpak's Docs "Sandbox permissions > Filesystem access"](https://docs.flatpak.org/en/latest/sandbox-permissions.html#filesystem-access)):

- **`--filesystem=host`**:
  - `/usr, /bin, /sbin, /lib{32, 64}, /etc/ld.so.cache, /etc/alternatives`, mounted at `/run/host` and provided by `--filesystem=host-os`.
  - `/etc`, mounted at `/run/host/etc` and provided by `--filesystem=host-etc`.
  - `/home`, `/media`, `/opt`, `/srv` and `/run/media`
  - **Reserved paths that are not included**: `/boot`, `/efi`, `/root`, `/sys`, `/tmp`, everything inside `~/.var/app` except `~/.var/app/$FLATPAK_ID` which has been granted access by default, `~/.local/share/flatpak` (very confusing, read more at [flatpak/flatpak#3637](https://github.com/flatpak/flatpak/issues/3637)), everything inside `/var` except `/var/lib/flatpak`, and `/var/lib/flatpak` itself.
- **`--filesystem=home`**: everything inside `~/` except `~/.var/app`.
- `--filesystem=xdg-*`: standardized paths. Recommended unless your system use different standard.
- `--filesystem=/some/dir` and `filesystem=~/some/dir`: arbitrary path to a directory inside sysroot or home.
- `:ro`: read-only. Think before granting read/write access for executable files.

- `--persist=` option , if used mindlessly, could lead to sandbox escape. Normally filesystem inside sandbox is setup as `tmpfs` so any data that's created inside the sandbox will be lost. Using could make files survive after application exiting in order to retain information serving the Flatpak application, not for sharing it with non-Flatpak applications outside the sandbox.

> Q: Some applications on Flathub by default, grant `--filesystem=host` or `--filesystem=home` permission, in some cases it's both. Is it safe?
>
> A:
>
> - [flatkill.org/2020](https://flatkill.org/2020), [flatpak/flatpak#3637](https://github.com/flatpak/flatpak/issues/3637) stated that a malicious Flatpak application can add malicious code into shell configuration file such as `.bashrc`, `.zshrc`, ... or add a `~/.bin/bash` wrapper around the real shell as mentioned by [alexlarsson on flatpak/flatpak#3637](https://github.com/flatpak/flatpak/issues/3637#issuecomment-673377849).
> - [Response to flatkill.org (2021-02-21)](https://tesk.page/2021/02/11/response-to-flatkill-org/#the-sandbox-is-still-a-lie) stated that this is inevitable for IDE, Media Creator/Editor Tools, ... in order to function smoothly.

> Q: Grant `--filesystem=home` permission is evil and should be avoid as much as possible?
>
> A:
>
> - [polzon's flatpak/flatpak#3637](https://github.com/flatpak/flatpak/issues/3637) provides a PoC to show that `filesystem=home` permission results in full permission escalation and render every security measure pointless. With this a malicious application can override any permissions inside `~/.local/share/flatpak/overrides/global` or `~/.local/share/flatpak/overrides/$FLATPAK_ID`. To my surprise, [`com.github.tchx84.Flatseal.json#L15`](https://github.com/tchx84/Flatseal/blob/9983e8ed205c30a30c79adbd3e9deb5e12dd0dc9/com.github.tchx84.Flatseal.json#L15) shows that this is how Flatseal used to manage permissions of other Flatpak applications.
> - According to [TingPing's comment on flatpak/flatpak#3637](https://github.com/flatpak/flatpak/issues/3637#issuecomment-635496998), novice users are responsible for their actions and they have to be _conscious_ about filesystem permissions. This is like how food poisoning can't be prevented so The Ministry of Health warns people has to be "smart and mindful" about they're going to eat, lol.
>
> **Confusion:** according to [Flatpak Docs "Sandbox Permissions > Reserved Paths"](https://docs.flatpak.org/en/latest/sandbox-permissions.html#reserved-paths), `$XDG_DATA_HOME/flatpak` or `~/.local/share/flatpak` is not available with `home, host, host-os, host-etc`. It can only be made available either by setting static permissions:
>
> 1.  Relative path: `--filesystem=~/.local/share/flatpak/overrides`
> 2.  Absolute path: `--filesystem=$HOME/.local/share/flatpak/overrides`.
> 3.  Standard path: `--filesystem=xdg-data` which grants access to `$XDG_DATA_HOME` or `$HOME/.local/share`.
>
> How is [flatpak/flatpak#3637](https://github.com/flatpak/flatpak/issues/3637) even possible if this is true? Does this path get added to reserved paths after the creation of this issue? I can't comment inside the issue since it has been limited to collaborators.

> Q: So users' should remove `--filesystem=host` and `--filesystem=home` permissions right? What's the catch?
>
> A:
>
> - [Response to flatkill.org (2021-02-21)](https://tesk.page/2021/02/11/response-to-flatkill-org/#the-sandbox-is-still-a-lie) stated that by doing so, applications can be unstable. Take GIMP as an example, it will lose some of its features. The only solution is to enforce _file chooser/portal_ but the devs say they would need to redesign the whole application.
> - [Response to flatkill.org (2021-02-21)](https://tesk.page/2021/02/11/response-to-flatkill-org/#the-sandbox-is-still-a-lie) proved that the number of Flatpak applications with sensible default permissions given by [flatkill.org/2020](https://flatkill.org/2020) is wrong. But, instead of easing the paranoid mind of users' by saying "we don't use them that often", Flatpak should create some types of warnings when user is about to install a Flatpak application so users' can understand more about them. But again, this can create a sense of false accusation that every `--filesystem=host`/`--filesystem=home` is evil, so warnings with reasons from application's devs are the most appropriate.

### Session Bus Policy

Be mindful when granting Session Bus permission:

- `org.freedesktop.Flatpak`.
- `org.freedesktop.systemd`
- `org.gnome.Terminal`
- `org.gnome.SessionManager`

> According to [`org.freedesktop.Flatpak.xml`](https://github.com/flatpak/flatpak/blob/main/data/org.freedesktop.Flatpak.xml), this permission includes a number of subpermissions (a.k.a interfaces) that can be used by different actors.
>
> - `org.freedesktop.Flatpak.SessionHelper` permission, expose **SessionHelper** interface, used by `flatpak run` command to bridge resources from the host system into Flatpak sandboxes.
> - `org.freedesktop.Flatpak.Development` permission, expose **Development** interface, allows any clients who have access to the SessionHelper can spawn a process on host system, outside any sandbox. Its methods:
>   - `HostCommand`: Runs arbitrary commands in the user's session outside any sandbox.
>   - `HostCommandSignal`: Sends a Unix signal to a process started by `HostCommand`.
>   - `HostCommandExited`: Signal emitted when a process started by HostCommand exits.
> - **SystemHelper** Manipulate Flatpak applications and runtimes that are installed system-wide. Luckily all of my Flatpak are installed at user-level.

[waffshappen's flatpak/flatpak#5161 (2022-03-11)](https://github.com/flatpak/flatpak/issues/5161) stated with a PoC that DBus permission `org.freedesktop.Flatpak` allow Flatpak applications spawning shells that can access files at user-level, results in a **sandbox escape**. [smcv's comment on flatpak/flatpak#5161](https://github.com/flatpak/flatpak/issues/5161#issuecomment-1326572478) admitted there are an unbounded number of permissions that currently are, and could be, sandbox escapes. Beside filesystem, Session Bus is one of them.

A simple workaround is [modifying permissions globally, via `~/.local/share/flatpak/overrides/global`](https://github.com/flatpak/flatpak/issues/5161#issuecomment-1326572478) so Flatpak sandbox can't be escaped via DBus interface anymore, but it could mess with the application's functionality somehow.

> Excessive default static permissions granting is the solution to make sure an application can function correctly within Flatpak's sandbox, which can increase the number of Flatpak users. If the popularity of Flatpak could keep rising. along with redesigning Flatpak apps utilizing portals, Flatpak repository maintainers will be stricter about accepting apps that require too many default static permissions. In my opinion, this can never be true, since the devs only do this out of users' concern, and if the majority of users' are ignorance or decided to stay silent, things won't change. Furthur more, there will be more and more static permissions granting for the development of new features.

### Advanced Permissions

- Limited syscalls.

## Misc

### Pros

- Branching (installing different versions of the same app, similar to containers)

- Decentralization (not really, Flathub is getting centralized)

- Rootless install.

### Cons

- Launching a Flatpak app is slower than launching a native app, since Flatpak has to mount dirs to contain and sandbox them, but it's not noticably slower because of the modern powerful hardware.

- Flatpak apps and runtime can contain long known security holes. [flatkill.org/2020](https://flatkill.org/2020) and - [Response to flatkill.org (2021-02-21)](https://tesk.page/2021/02/11/response-to-flatkill-org/) mentioned 1 security hole that takes too long to be plugged. I feared there are more holes that aren't mentioned or found.

- Runtimes can be bloated, occupy more disk space. The reasons are varied: some apps might be unmaintained, some can be neglected by lazy devs, [containers/bubblewrap](https://github.com/containers/bubblewrap) and [ostreedev/ostree](https://github.com/ostreedev/ostree) requires runtimes to be contained, ...

- Lack of data integrity checking mechanisms [flathub/flathub#1498](https://github.com/flathub/flathub/issues/1498):

  - "The built files match the publicly available source code of the software intended to be installed". This is also known as **reproducible build**.
    => Sadly it's [outside the scope of Flatpak](https://github.com/flathub/flathub/issues/1498#issuecomment-649098123).
  - "The downloaded files match the built files whose checksums are made publicly available". The **download files** refer to the files that're currently hosted on Flathub's server and users or client software need to fetch from the Internet.
    => There are integrity verification mechanisms that I'm unaware of.
  - "The installed files match the downloaded files whose checksums have been verified to be valid". The **installed files** refer to the ones that have been placed on the user's system after the download process.
    => Check `flatpak remote-info -c $FLATPAK_ID` against `flatpak info -c $FLATPAK_ID`.
  - "The installed files remain unchanged". This means the files should not be modified, corrupted or tempered during the application's functioning process. If a malicious Flatpak application have the neccessary

=> The goal of Flatpak is **distribution**, not **sandboxing**, but somehow Flatpak missionaries keep advertising its "sandboxing" capability.

## Reference

- [Michel Nallino's "Security, Privacy and Anonymity in Linux Mint"](https://nallino.net/stockage/security/Linux_Mint_Security.pdf)
