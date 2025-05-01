# Memory optimization on Linux kernel

<!-- tl;dr starts -->

With 16GB on-board RAM with no upgrade slot on a Lenovo Yoga Slim 7 Pro 2020, I'm suffering from various issues which result from lack of memory. 16GB has been the standard and bare-minimum for laptop's RAM size until now, but that has to change soon. Working as a programmer myself, my use cases ranges from opening multiple browser tabs to running tools inside code editor so it's very crucial to achieve optimal memory performance to ensure seemless work experience.

<!-- tl;dr ends -->

## TL;DR

I'm using Fedora KDE 40, `zram-generator` is installed by default.

```conf
# /etc/systemd/zram-generator.conf

[zram0]
zram-size = 16384
compression-algorithm = zstd
```

```conf
# /etc/sysctl.d/99-vm-zram-parameters.conf
# Reload by running `sudo sysctl -p`

# reduce memory used by file caching by a little
vm.vfs_cache_pressure=200
vm.swappiness = 180
vm.watermark_boost_factor = 0
vm.watermark_scale_factor = 125
vm.page-cluster = 0

# https://www.reddit.com/r/Fedora/comments/mzun99/comment/h1cnvv3
# https://www.reddit.com/r/Fedora/comments/mzun99/comment/hlik05o
# https://lonesysadmin.net/2013/12/22/better-linux-disk-caching-performance-vm-dirty_ratio

# since we're trying to populate zram block device as much as possible, dirty pages should be swapped as fast as possible
vm.vfs_cache_pressure=200
vm.dirty_background_ratio=1
#vm.dirty_background_bytes=0
vm.dirty_ratio=2
#vm.dirty_bytes=0
```

> TIPS: Run `sudo sysctl –p` to reload without restart machine.

## Application-specific solution

Programmers usually open a lot of tabs to read various information during their worktime. Many people, like me, forget to close them, results in wasting a lot of RAM.

To tackle this problem, install extensions like [Auto Tab Discard]() to "hibernate" unused tabs. The default behavior can be quite... murderous, so I have set interval to **30 minutes** and add the following websites to whitelist:

```txt
localhost, chatgpt.com, www.youtube.com

# You don't want your favorite music to be snapped death randomly right?
```

## Swap

### Knowledge

[Auto Tab Discard]() it's simply not enough for my use cases. During the service of my first-encoutered Linux distro, [Ubuntu 22.04 Jammy](https://releases.ubuntu.com/jammy/), I've known about the concept of:

#### Memory

- Kernel buffers, for network stacks, SCSI queues, ...
- Applications.
- Disk cache. According to [Linux Ate My RAM](https://www.linuxatemyram.com), a portion of RAM that's unused by buffers or applications will be utilize as disk cache. Running `free -m` would show the disk cache as _available_.

```txt
> free -m
          total     used      free    shared    buff/cache   available
Mem:      15337     11415     1653      164     3288         3922
Swap:     8191      8173      18
```

_Q: When memory is running low, what should OS do?_

- **Kernel buffers** must stay in memory (simply because they have to)
- **Applications** can be paged out to _swap_. This swap can be hard disk, which leads to performance hit, or RAM disk to reduce the negative impact.
- **Disk cache** can be retrieved, results in performance drop.

#### Virtual memory

- **Memory management technique**/**abstraction** that provides each process illusions of having its own large, contiguous block of memory.
- **Storage allocation scheme** in which _secondary memory_ (SSD/HDD, slow, non-volatile) can be addressed as though it were part of the _main memory_ (a.k _physical memory_) (RAM, fast, volatile).

Either way: program whose memory requirement is much larger than _physical memory_ can run without issue.

- A process is broken into a number of pieces (later called _pages_)
- Pages need not to be stored contiguously in _physical memory_. Pages can be stored either inside:
  - _physical memory_ if MMU "accessed them frequently"
  - _secondary memory_ (a.k.a swap space) when pages got "swapped out" because MMU "deemed them inactive".
- When they are needed, the pages are "swapped in" back from _secondary memory_ to _physical memory_. This "swapped in", "swapped out" (ooh, wax on, wax off) process is called "paging".

Virtual memory is managed by _Memory Management Unit (MMU)_. During the course of execution of a process, MMU maintains a "page table" that maps _virtual (memory) addresses_ to _physical (memory) addresses_. Process can see a contiguous block of memory inside _virtual address space_ but it's actually not the case when they got mapped into _physical address space_.

### Practice

Okay, that's little over of some people's head. So what do we do with this maginificent feature?

There are many factors to consider:

#### Secondary memory

There are currently 3 secondary memory solutions: **swap on disk**, **zram** and **zswap**:

- Swap on disk create block device on disk, zram is create compressed block device in RAM, zswap creates compressed RAM cache (still requires block device on disk like swap on disk).
- Due to IO speed of each hardware: zram, zswap > swap on disk => Use zram, zswap. **zram is my current choice**.

To set the size for zram device using `zram-generator`, change `zram-size=` entry inside `/etc/systemd/zram-generator.conf`. According to [Arch Linux Wiki's "zram > Usage as swap"](https://wiki.archlinux.org/title/Zram#Usage_as_swap), this size is the "maximum uncompressed amount of data" that zram device can store, _not_ the maximum compressed size.

_Q: What is the optimal size for zram device?_<br/>
A: Half of total RAM, in my case, 8GB. But it's better to set it as high as possible, usually same as your total RAM. **I have set mine to 16GB after experiencing my browsers getting killed by OOM Killer**. This is backed by [kurushimee's zram guide](https://github.com/kurushimee/configure-zram), consider he's a game developer and his use cases are to run games and game engines.

#### Compression algorithm

- **lz4**: fastest compress/decompress speed, good compression ratio (1:3)
- **lzo-rle**: same as **lz4** but with **RLE - Run-Length Encoding** in addition, better if memory is filled with repetitive data.
- **zstd**: good compress/decompress speed, excellent compression ratio (1:4). Many application use zstd, for example [btrfs](https://docs.kernel.org/filesystems/btrfs.html) (might be a little biased since both btrfs and zstd are from Facebook), [borg](https://www.borgbackup.org), mksquashfs, ... => **zstd is my current choice**

> TIPS: Run `cat /sys/block/zram0/comp_algorithm` to print available compression algorithms for your system.

_Q: What is the most optimal compression algorithm?_<br />
A:

- External evaluation:
  - [zram tuning benchmarks on Reddit](https://www.reddit.com/r/Fedora/comments/mzun99/new_zram_tuning_benchmarks/)
  - ![zram compression algorithm comparision](https://i.imgur.com/EDLZNUZ.png)
- Internal evaluation: there is no easy way, can only by done by trial-and-error for your specific hardware and software. I'm using `zstd` now because of its compression ratio being the highest at the cost of CPU powers.

#### Kernal options

Read [Documentation for /proc/sys/vm/](https://docs.kernel.org/admin-guide/sysctl/vm.html) for more information.

Swap strategy controlled by `vm.*` settings:

- `vm.swappiness=[0-200]`: how likely is the system is going to start swapping.

  Example:

  - `vm.swappiness=100`(or more than 100) means kernel will swap aggressively.
  - `vm.swappiness=0` means kernel will only swap to prevent out-of-memory (OOM).

  According to [this formula](https://www.kernel.org/doc/html/latest/admin-guide/sysctl/vm.html#swappiness) on kernel's docs, if we assumes RAM is faster than disk 10x time (actually much much more), the value would be `vm.swappiness=180`. Some even set `vm.swappiness=200` but I think you should only do for benchmarking purpose.

  > WARNING: Swapping is bad in virtual environment. Use `vm.swappiness=0` when setting up virtual machine.

- `vm.page-cluster=[0,1,2,3]`: controls the number of pages up to which consecutive pages are read in from swap in a single attempt. `vm.page-cluster=0` limits that to 1 page per attempt, which arrives lower latency.

- `vm.vfs_cache_pressure=[0-inf]`: the higher the value over 100, the more likely the kernel will reclaim the memory of disk caching.

- `vm.dirty_background_ratio=[0-100]`: the % of system memory that can be filled with “dirty” pages — memory pages that still need to be written to _secondary memory_ — before the `pdflush/flush/kdmflush` background processes kick in to write it to _secondary memory_.

  My example is `vm.dirty_background_ratio=10`, so if my machine has 16GB of memory, that's 1.6GB of data that can be sitting in RAM, before something is done.

- `vm.dirty_ratio=[0-100]`: the maximum amount of system memory that can be filled with "dirty" pages before everything must get committed to _secondary memory_. It's logical to say that `vm.dirty_ratio` must be larger than `vm.dirty_background_ratio`. When the system gets to this point, all new I/O blocks until dirty pages have been written to disk. This is often the source of long I/O pauses, but is a safeguard against too much data being cached unsafely in memory.

- `vm.dirty_background_bytes=0` and `vm.dirty_bytes=0`: the value in bytes of above options. If you set the \_bytes version, the \_ratio version will become 0, and vice-versa.

  > See statistics on page cache. Example:
  >
  > ```
  > > cat /proc/vmstat | grep -E "dirty|writeback"
  >
  > nr_dirty 464
  > nr_writeback 0
  > nr_writeback_temp 0
  > nr_dirty_threshold 216676
  > nr_dirty_background_threshold 108206
  > ```
  >
  > In this case, I have 464 dirty pages waiting to be written to secondary memory.

## References

- [Bob Plankers's "Adjust vm.swappiness to Avoid Unneeded Disk I/O"](https://lonesysadmin.net/2013/12/11/adjust-vm-swappiness-avoid-unneeded-disk-io/)
- [Bob Plankers's "Better Linux Disk Caching & Performance with vm.dirty_ratio & vm.dirty_background_ratio"](https://lonesysadmin.net/2013/12/22/better-linux-disk-caching-performance-vm-dirty_ratio)
- [GeeksForGeeks's "Virtual Memory in Operating System"](https://www.geeksforgeeks.org/virtual-memory-in-operating-system/).
- [Arch Linux's Wiki "zram: Using zram-generator"](https://wiki.archlinux.org/title/Zram#Using_zram-generator)
