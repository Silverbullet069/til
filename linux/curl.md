# `curl` command

<!-- tl;dr starts -->

My favorite tool to download files on Internet. It's also known as "Client for URL".

<!-- tl;dr ends -->

## `curl -o [FILE]` vs. `curl > [FILE]`

| Features                                 | `curl -o [FILE]` | `curl > [FILE]` |
| ---------------------------------------- | ---------------- | --------------- |
| Built-in?                                | Yes              | No, shell       |
| Create parent directories?               | Yes              | No              |
| Retain file's permission and timestamps? | Yes              | No, umask       |
| Clean leftover files if download failed? | Yes              | No              |
