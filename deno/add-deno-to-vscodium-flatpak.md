#

<!-- tl;dr starts -->

Running `deno` and `deno` dependency projects - [ComicCrawler](https://github.com/eight04/ComicCrawler), [deno_vm](https://github.com/eight04/deno_vm), [worker-vm](https://github.com/eight04/worker-vm) inside VSCodium Flatpak with harden permissions is more secure than running them inside my Fedora system.

<!-- tl;dr ends -->

Add read-only `~/.deno/env` permission to VSCodium Flatpak, and `~/.deno/bin/deno` will be automatically added into the shell's `$PATH`.
