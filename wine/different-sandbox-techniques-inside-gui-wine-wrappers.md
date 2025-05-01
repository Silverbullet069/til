# Different Sandbox Techniques Inside GUI Wine Wrappers

<!-- tl;dr starts -->

There are many GUI Wine wrappers in the market. Their core functions are pretty much very similar so I will focus on the security, more specific sandbox capability, the most crucial factor when I'm choosing one.

<!-- tl;dr ends -->

## [Lutris](https://github.com/lutris/lutris)

### Wine Sandbox is a lie!

I have been deceived all this time. According to [danieljohnson2's comment on lutris/lutris#4755](https://github.com/lutris/lutris/issues/4755#issuecomment-1464875996), Wine Sandbox is a separate place for Wine to put standard directory which typically found inside a Windows environment (e.g. `My Documents`, `Downloads`, ...) under a dedicated environment that doesn't interfere with directories lie inside other Wine prefixes.

### Lutris runners built-in sandbox capability

Interesting, [T-X, the author of lutris/lutris#4755](https://github.com/lutris/lutris/issues/4755#issuecomment-1462486397) stated that he has tried to run a malicious executable which executes Linux syscalls usable from Wine to check if he can read `~/.ssh`. Surprisingly, for "System 8.0" runner options, he can, but not for other runners like [Wine provided by GloriousEggroll](https://github.com/GloriousEggroll/wine-ge-custom) and Wine dedicated to Lutris.

=> Wine runners before version 9 unreliable and unpredictable.

The release of [Open-Wine-Components/umu-launcher](https://github.com/Open-Wine-Components/umu-launcher) which is formerly known as [GloriousEggroll/proton-ge-custom](https://github.com/GloriousEggroll/proton-ge-custom), add a generic [pressure-vessel-wrap](https://gitlab.steamos.cloud/steamrt/steam-runtime-tools/-/blob/main/pressure-vessel/wrap.1.md) support. This tool is what Steam Linux used to enforce isolation, down below it's just a wrapper around [containers/bubblewrap](https://github.com/containers/bubblewrap), the sandbox technology used by Flatpak.

If user used "System 9.0 (default)" option, it has UMU by default.

## [Bottles](https://github.com/bottlesdevs/Bottles)

[orowith2os's comment on lutris/lutris#4755](https://github.com/lutris/lutris/issues/4755#issuecomment-1639363760) stated that Bottles have its sandbox feature, it's actually `flatpak-spawn` when checking its [`sandbox.py#L92`](https://github.com/bottlesdevs/Bottles/blob/9132667ae41a04769b286a09471306ba4deed980/bottles/backend/managers/sandbox.py#L92) file inside `bottlesdevs/Bottles` repository. And guess what? Deep down it's just `bwrap`. It's recommended to use `flatpak-spawn` due to its high-level design compare to `bwrap` which is low-level and lead to unforeseen consequences (puns intended).

## [Firejail](https://github.com/netblue30/firejail)

Firejail has a number of peer-reviewed default profiles that's available as the base of your specific use case:

- Lutris has one profile as well and it's [being actively maintained](https://github.com/netblue30/firejail/commits/e142786bfdac42f23878939f7ee240b4d0fcd8bd/etc/profile-a-l/lutris.profile) lately.

- There is also a [Wine profile](https://github.com/netblue30/firejail/blob/master/etc/profile-m-z/wine.profile).

### Best practices

- Make sure that the program is really running in Firejail: `firejail --list`.
- Disable network.
- Disable D-Bus access.
