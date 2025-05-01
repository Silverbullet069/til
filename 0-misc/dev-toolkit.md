# My developer toolkit documentation

## Table of Contents

1. [Introduction](#introduction)
2. [To-Do List](#to-do-list)
3. [Applications](#applications)

- [3D Design](#3d-design)
- [API platform](#api-platform)
- [Application Deployment Frameworks](#application-deployment-frameworks)
- [Cloud](#cloud)
- [Code Editor](#code-editor)
- [Container image builder](#container-image-builder)
- [Data Processor](#data-processor)
- [Database](#database)
- [Diagram Editor](#diagram-editor)
- [Domain hosting platform](#domain-hosting-platform)
- [IDE](#ide)
- [Network interceptor](#network-interceptor)
- [Package Manager and Version Manager](#package-manager-and-version-manager)
- [Programming Language Binary](#programming-language-binary)
- [Sitemap Generator](#sitemap-generator)
- [SQL client](#sql-client)
- [Version Control](#version-control)
- [Virtualization](#virtualization)
- [Web Server](#web-server)

4. [Miscellaneous](#miscellaneous)

## Introduction

This is 2nd attempt to make my own **Developer Toolkit** documentation based on the following references:

- ...

In this documentation, I wil use a series of tags to avoid dupllications as much as possible.

## To-Do List

- Create a script that automatically create a template for tagging in my docs by pressing a global custom hotkey.

## Applications

### 3D Design

1. Blender [#ubuntu2204]() [#fedorakde40]() [#prebuilt]()

- Src: `~/FOSS/blender-4.2.2-linux-x64`
- Symlink to: `~/.local/bin`

### API platform

1. Postman [#ubuntu2204]() [#fedorakde40]() [#vscodeext]()

### Application Deployment Frameworks

1. Ansible [#considering]()

2. Nix [#considering]()

### Cloud

1. `rclone` [#fedorakde40]() [#dnf]()
2. `google-cloud-cli` [#ubuntu2204]() [#prebuilt]()

### Code Editor

1. Visual Studio Code (VSCode) [#ubuntu2204]() [#deb]()
   > [!NOTE]
   > There are 3 VSCode versions:
   > Code-OSS: from Microsoft, OSS code
   > VSCode: from Microsoft - Code-OSS + Proprietary stuff + Telemetry
   > VSCodium: from community - Code-OSS + OSS stuff + no telemetry. Con is smaller ext store.

> [!TIP]
> Column Selection
> Windows: `Alt + Click`
> Linux: `Alt + Shift + Click`

2. VSCodium [#fedorakde40]() [#flatpak]()
   > [!CAUTION]
   > Using Flatpak version with its sandboxing and permission hardening make prone some issues so besure to check [Flatpak VSCodium GitHub Repository](https://github.com/flathub/com.vscodium.codium?tab=readme-ov-file#flatpak-vscodium) to troubleshoot and fix.

- Enable running X11 applications from Wayland session.
- Restrict access to host filesystem, grant ad-hoc read-only access later:
  - To use SDKs such as `node` or `go`, you shouldn't give explicit access. A more elegate approach is to install the Flatpak version of these SDKs and then add `FLATPAK_ENABLE_SDK_EXT` environment variable to VSCodium.
```sh
flatpak install flathub --user org.freedesktop.Sdk.Extension.golang # if prompted, choose the latest branch
flatpak install flathub --user org.freedesktop.Sdk.Extension.node22 # might be depreciated in the future
flatpak override --user --env FLATPAK_ENABLE_SDK_EXT=golang,node22 com.vscodium.codium
```

- I'm using KDE and happens to disable `kwallet`, KDE will use `GNOME Keyring` as fallback solution, but it had issue with VSCodium. Follows _Migrate from GNOME Keyring to KeePassXC guide in Post Installation documentation_ then:

  - Add `--password-store="gnome-libsecret"` into all Flatpak desktop files [#desktop]()
  - Persist the value of `password-store` by `Ctrl + Shift + P > Preferences: Configure Runtime Arguments`, add `"password-store":"gnome-libsecret"`
  - Tested persistence after reboot.

- Somehow, PyLance extension does not working in VSCodium, so I uninstalled it, install [DetachHead/basedpyright](https://github.com/DetachHead/basedpyright) and change Python Language Server to **Default**.
- Using host system's shell prose many problems, including not be able to use Language Server, so I only use shell from environment created by VSCodium. It uses Bash by default and I add some personal tweaks to it in `.bashrc`.

[Monitor the issue](https://stackoverflow.com/q/75345501/9122512)

- Add `--ignore=E302,E265` to `python.formatting.autopep8Args` to ignore two lines between outer layer comment and code

> [!CAUTION]
> Due to some weird behavior, VSCodium startup didn't prompt KeePassXC unlocking so it keeps failing GitHub authentication. My assumption is that I didn't add the `--password-store="gnome-libsecret` to all of `Exec=` line in custom `.desktop` file.

- View VSCode Marketplace inside VSCodium UI by using a custom `product.json`:
  - [How to use a different extension gallery](https://github.com/VSCodium/vscodium/blob/master/docs/index.md#how-to-use-a-different-extension-gallery)
  - [For Flatpak user, where is the custom `product.json` be putted?](https://github.com/flathub/com.visualstudio.code-oss/issues/11#issuecomment-782694865)

> [!CAUTION]
> DO NOT TRY TO INSTALL EXTENSION VIA `.vsix` FILE SINCE IT CAUSES VERSION CONFLICTS!
> If you must due to some reasons, install VSIX Manager.
> There for, you can skip the API modifications in `home/$USER/local/share/flatpak/app/com.vscodium.codium/x86_64/stable/.../files/share/codium/resources/app/product.json`. Know which is missing by checking the Output tab then Window.
> It will be overriden after VSCodium Flatpak is updated thou.

- Add a simple Fish function to run VSCodium from terminal.
- Extension list:
  - GitHub Pull Requests
  - GitHub Copilot
    > If install via `.vsix` file, follow [this workaround by ustas-eth](https://github.com/VSCodium/vscodium/discussions/1487). Haven't tested yet.
  - GitHub Copilot Chat
    > If install via `.vsix` file, follow [this workaround by melroy89](https://github.com/VSCodium/vscodium/issues/1753#issuecomment-2064992100), failed at the login step. Also [TimTheBig's guide](https://github.com/VSCodium/vscodium/issues/1852#issuecomment-2065300804)
  - IntelliCode API Usage Examples

**Bugs:**

- VSCodium says it can't connect to GNOME Libsecret although you have changed it to KeepassXC
  => A: KeePassXC must be unlocked manually before that.

[Stefan Judis's "Emmet VS Code bindings to level up HTML editing"](https://www.stefanjudis.com/blog/emmet-vs-code-bindings-to-level-up-html-editing/)

### Data Processor

1. Miller CLI [#considering]()

### Database

1. MySQL Server [#fedorakde40]() [#officialrepo]()

- Create a new account with broad superuser privileges that akin to `root`.
- Change `root` account password.
- Autostart on boot [#systemd]()

[DigitalOcean's "How To Create a New User and Grant Permissions in MySQL"](https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql)

2. MongoDB [#fedorakde40]() [#officialrepo]()

- Autostart on boot [#systemd]()

**Bug:** <br />

- File conflicting when install `mongodb-mongosh` after `mongodb-mongosh-shared-openssl3`
  => Assumption: You don't need `mongodb-mongosh`.

### Diagram Editor

1. Visual Paradigm [#ubuntu2204]() [#prebuilt]()

- Standardized.
- Big and slow.

2. `diagrams.net` (formerly `draw.io`) [#saas]()

- Fast, cross-platform
- Unstandardized, automation features not available, had to do some manually, nitty-witty things.

3. PlantUML [#considering]()

[Comparisons between Text to Diagram tools](https://text-to-diagram.com/)

> [!NOTE]
> You can also create diagrams using ASCII chars. It's better when being used to visualize the cont
> rol flow or data flow of a piece of code in terms of code comment.

### Domain hosting platform

1. Vercel
2. Cloudflare Pages
3. Hover

### IDE

1. Android Studio [#ubuntu2204]() [#prebuilt]()

- Big, slow, complex to setup.

2. Visual Studio [#ubuntu2204]() [#official]()

- Big, not necessary.

3. RStudio [#ubuntu2204]() [#deb]()

4. WebStorm

- Haven't tried yet. But now it's free for non-commercial use.
- Might fix that TypeScrpt problem.

### Network interceptor

1. HTTPToolkit [#ubuntu2204]() [#prebuilt-binary]()

### Package Manager and Version Manager

1. `npm` [#ubuntu2204]() [#nvm]()

- There are 3 ways to install a local package:

```sh
# Method 1: npm install
# Run either 1 of these commands
npm install /SOME_PATH                # symbolic link
npm install --save-dev /SOME_PATH     # copy

# ============================================================================
# Method 2: npm link
# More verbosely, shows that npm creates 2 symbolic links
cd ./PACKAGE_DIR && npm link
cd ./PROJECT_DIR && npm link PACKAGE_NAME

# ============================================================================
# Method 3: npm pack + package.json
# Pros: it also installs sub-dependencies of local package into PROJECT_DIR's npm
# Personal insight: so far, this is the best approach

cd ./PACKAGE_DIR && npm pack
# Create a file: PACKAGE_NAME-VERSION.tar.gz

cd ./PROJECT_DIR && mkdir tmp && mv SOME_DIR/PACKAGE_NAME-VERSION.tar.gz .

nano package.json
# "dependencies": {
#   "my-package": "file:/./tmp/PACKAGE_NAME-VERSION.tar.gz"
# }

[ npm i | npm install | yarn ]
```

- When installing a local package, `npm` creates a symlink to that folder
  `npm install /SOMEPATH`
- Global package list:

```sh
# npm list -g
npm-check-updates
yo
generator-code
typescript
ts-node
yarn
(...will update more)
```

> [!TIP]
> From `npm` version 10.6.0 to go, progress bar is removed while running `npm install`. Workaround this can be made by adding `--loglevel http` option.

2. `nvm` [#ubuntu2204]() [#official]() [#fedorakde40]() [#fisher]()

- 1st setup: Use in combination of [nvm-sh/nvm](https://github.com/nvm-sh/nvm) and [FabioAntunes/fish-nvm](https://github.com/FabioAntunes/fish-nvm) (Ubuntu)
- 2nd setup: Use [jorgebucaran/nvm.fish](https://github.com/jorgebucaran/nvm.fish).

> [!NOTE]
> Using 1st setup can lazy-load `npm`, `npx`, `node`, `yarn`. First command takes more than a second to complete.
> Using 2nd setup there is no lazy-load, but since the script is made with Fish, it's blazing fast so there is no overhead during startup. Also had to add a cronjob to update node version regularly. [#cron]()

```sh
# crontab -e
...
3 0 * * mon /home/$USER/.dotfiles/0-automation-script/update-node-lts.fish
...
```

3. `pip` [#builtin]()

> [WARNING]
> Accidentally install a local Python project into global environment instead of virtual environment can leave a lot of unused packages.
> Determine which `pip` packages are currently used/unused by rename all `__pycache__` directory in all packages. After some time (at least a month, to be sure) which package recreate new `__pycache__` is the one that's used by system.

4. `yarn` [#npm]()

### Programming Language Binary

1. Python and Jupyter Notebook [#builtin]()

[Differences between **pyenv**, **virtualenv**, **anaconda**](https://stackoverflow.com/a/39928067)

2. Java [#considering]()

### Sitemap Generator

### SQL client

1. DBeaver [#ubuntu2204]() [#deb]() [#fedorakde40]() [#flatpak]()

- Disable Pulseaudio Sound Server, Remote Login Access permissions.
- Disable **All User Files** access, restrict to `~/.local/share/DBeaverData` and `~/Downloads`.

2. HeldiSQL [#windows10]() [#exe]()

- Autocompletion after character input is not supported.
=> Solution: Make an AutoHotkey script that auto send `Ctrl` + `Space` right after typing a-z 0-9 and some special character.

### Version Control

1. Git [#ubuntu2204]() [#fedorakde40]() [#built-in]()

- Config SSH key to fix password auth not working due to new GitHub's security policy.
- [Gabriel Cruz's "Clone a specifc folder from a GitHub Repository"](https://medium.com/@gabrielcruz_68416/clone-a-specific-folder-from-a-github-repository-f8949e7a02b4)

> [!TIP]
> Fork a lot. It's the way to contribute to OSS.

2. Git LFS [#built-from-source](https://github.com/git-lfs/git-lfs?tab=readme-ov-file#from-binary)

- Git CLI extension to manage large files.
- User with GitHub Free and GitHub Pro plan can store at most 2GB.

3. `git-crypt` [#built-from-source](https://github.com/AGWA/git-crypt/blob/master/INSTALL.md)

- Git CLI tool to encrypt files before pushing to GitHub

> **NOTE:** It can't be used with Git LFS. See this [SOF answer](https://stackoverflow.com/a/64488767).

4. [hackjutsu/Lepton](https://github.com/hackjutsu/Lepton) [#ubuntu2204]() [#fedorakde40]() [#appimage]()

It's GUI client to GitHub Gist.

- Create `~/.dotfiles/0-automation-script/lepton.sh` that utilizes:
  - `/usr/include/linux/input-event-codes.h` from [ReimuNotMoe/ydotool](https://github.com/ReimuNotMoe/ydotool)
  - [lucaswerkmeister/activate-window-by-title](https://github.com/lucaswerkmeister/activate-window-by-title)
    => Apply settings inside its custom developer tools to Lepton UI. (It's an Atom-based application).

**Bug**:

- Unmaintained, buggy, leak secrets in log?

### Virtualization

1. Genymotion [#ubuntu2204]() [#fedorakde40]() [#prebuilt]()

**Bug:**

- UI scaling issue  => Add `QT_SCALE_FACTOR=2` to its custom `.desktop` file. [#desktop]()

### Web Server

1. Apache `httpd`

- Check module list, run `apache2ctl -M`
- If the module hasn't been installed before, `sudo a2enmod [MODULE_NAME]`
- Check Apache config file [`/etc/apache2/apache2.conf`](https://gist.github.com/Zeokat/3b5c1273a7da48e1ad94) (`httpd.conf` is the legacy config file but it's depreciated) and comment out line `#LoadModule MODULE_NAME modules/MODULE_NAME.so`
- Restart Apache server: `sudo service apache2 restart`
- Use `<IfModule ...></IfModule>` tag to only use the module if it's installed. This is to prevent site brackage when switching between different environments.

## Miscellaneous

[Opensource's Install Ansible Package](https://opensource.com/article/20/9/install-packages-ansible)
[FrontPageLinux's Ansible Beginner Guide automate the pain away](https://frontpagelinux.com/tutorials/ansible-beginner-guide-automate-the-pain-away/)
[LinuxConfig's How to setup GNOME using Ansible](https://linuxconfig.org/how-to-setup-gnome-using-ansible)
[mtlynch's Nix first impression](https://mtlynch.io/notes/nix-first-impressions/)
