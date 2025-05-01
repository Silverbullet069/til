# Rollback installation/uninstallation made by `dnf` package managers

<!-- tl;dr starts -->

When I was installing ROCm on Fedora following a [guide on Medium](https://medium.com/@anvesh.jhuboo/rocm-pytorch-on-fedora-51224563e5be) to run ROCm-support applications on my Vega 8 APU, I was unease by the sheer amount of packages that are waiting to pollute my global environment. I need a way to revert these changes.

<!-- tl;dr ends -->

Simply, run `dnf history list` to list all the transaction:

```txt
> dnf history list

ID Command line            Date and time       Action(s) Altered
 4 dnf install rocm-hip    2024-12-15 19:26:37                16
 3 dnf install rocm-clinfo 2024-12-15 19:22:56                 1
 2 dnf install rocm-opencl 2024-12-15 19:22:25                10
 1 dnf update              2024-12-15 18:05:56                 6
```

Run `dnf history rollback 1` to undo all the transactions performed **AFTER** the `dnf update` transaction.

Next time, I wouldn't listen to some [random Redditers](https://www.reddit.com/r/Fedora/comments/1ajhds6/comment/kp0zps7) provides unofficial method to install highly sophisticated tools like ROCm.
