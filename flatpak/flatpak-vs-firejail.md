# Flatpak vs Firejail: A Comparison of Linux Sandboxing Solutions

<!-- tl;dr starts -->

After reading about [containers/bubblewrap or `bwrap`](https://github.com/containers/bubblewrap), [`flatpak-spawn`](https://docs.flatpak.org/en/latest/flatpak-command-reference.html#flatpak-spawn) (which is [containers/bubblewrap](https://github.com/containers/bubblewrap)'s abstraction), [netblue30/firejail](https://github.com/netblue30/firejail), there are only 2 contestents remained: Flatpak and Firejail.

<!-- tl;dr ends -->

I should write a "Should Firejail be used?" TIL but it's better to compare it to a long-history and high popularity sandboxing solution like Flatpak/`flatpak-spawn`/``bwrap`.

## TL;DR

VM (VirtualBox/VMware) > Flatpak (`flatpak-spawn`, `bwrap`, `pressure-vessel-wrap`) > Firejail.

## 1. Use cases

Firejail is just a mere sandboxing solution, a wrapper, an outer layer for programs installed via Linux distro's package manager (`apt`, `dnf`, `yum`, `pacman`, ...), package managers specific for packages from programming languages (`npm`, `yarn`, `pip`, `cargo`, ...) and executables compiled from source code or pre-built binaries that's built by author (`tar.gz, .bundle, ...`).

Firejail can be expanded to privileged programs and CLI utilities.

---

Flatpak is a full development/building/distribution/running framework. Flathub is the centralized distribution solution for Flatpak. Applications can be run cross-distro thanks to the running framework.

Flatpak can not run privilleged program (do not mistaking installing at system-level is the same as running as privileged), or CLI utilities. In this case you could use `bwrap` command directly. My Fedora KDE has it.

> [Stremio for Linux](https://www.stremio.com/downloads) only available either as:
>
> - Flatpak
> - Debian-based package
> - Arch-based package
> - Binary compiled from source code.
>
> I'm using Fedora currently, only the first and the last methods works for me. I could either build the app from source using last method and wrap it around with Firejail, or just use Flatpak with tailored permissions.

## 2. Up-to-date

For other methods, up-to-date is always. But for Flatpak, some do, some don't. Even though Flatpak depends entirely on the updates of the same application on other platforms, it's up to the Flatpak distributor to build a new Flatpak runtime/application that reflects the update.

E.g. [`net.lutris.Lutris.yml#L747`](https://github.com/flathub/net.lutris.Lutris/blob/9cd2beaee65c2de6f60583f73e2a4807959e2a16/net.lutris.Lutris.yml#L747) indicates Lutris Flatpak is built based on the source code on official repository of Lutris, same applies with [`com.parsecgaming.parsec.yml#L64`](https://github.com/flathub/com.parsecgaming.parsec/blob/96fd292bee4b4d0ca61bb786867f1ab5f2407a1b/com.parsecgaming.parsec.yml#L64)

Some applications can be lagged behind due to reason unknowned to me. My speculation is that new updates tend to be error-prone and Flatpak application developers/distributors needs to look into change log and release notes of the new updates to identify the bugs.

> **Controversial:** [Flatkill/2020](https://flatkill.org/2020) points out Flatpak runtime maintainers can neglect security updates for a long time. I don't know if this is still the case till the time this post is written.

## 3. Dependencies isolation

Firejail sandboxed applications still use OS libraries, but Flatpak use their own libraries and dependencies

## 4. Permission models

Flatpak permissions are user-friendly and easy to tweak. There are many permissions managers such as[tchx84/Flatseal](https://github.com/tchx84/Flatseal), [`flatpak override`](https://docs.flatpak.org/en/latest/flatpak-command-reference.html#flatpak-override), or "KDE System Settings's Flatpak Permissions".

But sometimes I can feel it can be too abstract and black-boxed heavily. User can be misunderstand or completely clueless about a certain permission. Flatpak can only handle a small, hard-coded Seccomp filters.

---

For Firejail, user defines permissions by writing entries into a _profile_. It's much more verbose and fine-grained than Flatpak's `.toml`-like that defines permissions of the Flatpak app. Firejail can customize Seccomp filters.

Firejail's handling of filesystem sandboxing:

- _whitelist all, blacklist some_
  **Cons:** Lead to missing blacklist entries regarding sensible directories.

- _blacklist all, whitelist some_ (which is what Flatpak used also)
  - **Pros:** maximum transparency for filesystem permissions.
  - **Cons**: for some applications resource requirements can have high complexity, lead to tedious list of static permissions or missing whitelist entries that are essential for the stability of the Flatpak application. Dilemma, when directories that need to be both whitelisted and blacklisted often arised as well.

## 5. Sandbox configuration maintainers

For Flatpak applications, it's the _Flatpak packagers/maintainers/distributors_ who are taking this job. These are the people who create and maintain Flatpak repositories on FlatHub (e.g. [flathub/net.lutris.Lutris](https://github.com/flathub/net.lutris.Lutris)), more specifically: _Flatpak packages_ hosted on Flathub applications from other distribution mechanisms:

- Building: Flatpak distributors build the _Flatpak format_ `.flatpak` from source code from application's official repository, its dependencies, default permissions for sandbox mechanisms, ... (e.g. [org.flameshot.Flameshot-12.1.0.x86_64.flatpak](https://github.com/flameshot-org/flameshot/releases/download/v12.1.0/org.flameshot.Flameshot-12.1.0.x86_64.flatpak)) on Flathub server and hosts on themselves. They do this by writing a `$FLATPAK_ID.yml` manifest file.

- Maintaining: Flatpak distributors must rebuild the Flatpak package to reflect the release of new versions from official repository. They do so by updating the `$FLATPAK_ID.yml` manifest file to adapt to new changes, running existing tests and writing new tests.

---

For Firejail, things are not so good:

- Profiles are maintained by communities who want to make a tight sandbox for their applications, usually not by the original authors/maintainers themselves if they deemed security is a trivial matter. Without the deep knowledge about the application, the profile maintainers have to test new restrictions every time there is a PR. There are applications whose profile has been neglected for years.

- Not every applications out there have their own Firejail profile community. Individuals who are mindful about security have to take their time to learn about Firejail to write their own profile file, but eventually they will have a clear and better understanding about Firejail.

## 6. Popularity

[In 2021-04-29, Alpine Linux removed `firejail` package due to its "atrocious security record" of being an SUID application.](https://gitlab.alpinelinux.org/alpine/aports/-/issues/12643)

**UPDATE:** At the time of writing this post, [Firejail has been existed inside Alpine Linux's repository.](https://voidlinux.org/packages/?arch=x86_64&q=firejail)

> **SUID application**: Normally a program runs with the permissions of the user who started it. But, an executable with its setuid permissions bit set, on the other hand, runs as the user that owns the executable file. Example:
>
> ```sh
> > ll /bin/mount
> -rwsr-xr-x. 1 root root 48K Jul 20 07:00 /bin/mount*
> ```
>
> Any mere users can run `/bin/mount` to auto mount filesystems, which is a perfectly normal system operation. But not so much in the case of a setuid executable being compromised in a manner that allows an attacker to trick it into launching another program/code since that program/code then also runs with root privileges.
>
> But for some reason, I can't reproduce it on my Fedora. It must be the work of security measures that've been implimented later, which explains how `firejail` is re-added into Alpine Linux's repository.

[Firejail does not present in Canonical-maintained repository of Ubuntu, only in Universe repository](https://forums.linuxmint.com/viewtopic.php?p=2166875#p2166875)

UPDATE: It's still not found on [Ubuntu Packages search results](https://packages.ubuntu.com/search?keywords=firejail&searchon=names&suite=oracular&section=all).
