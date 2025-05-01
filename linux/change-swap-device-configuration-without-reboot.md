# Change Swap Device Configuration Without Reboot

<!-- tl;dr starts -->

Sometimes I would like to test different zram compression algorithms on a specific use case without the need to restart machine.

<!-- tl;dr ends -->

I'm using `zram-generator` so I change zram configuration at `/etc/systemd/zram-generator.conf`:

```conf
[zram0]
zram-size = 16000
compression-algorithm = zstd
```

Reset zram device:

```sh
sudo systemctl restart systemd-zram-setup@zram0.service
```

Kernel parameters about swap can be change independently at `/etc/sysctl.d/99-vm-zram-parameters.conf`

```conf
vm.swappiness=180
vm.watermark_boost_factor=0
vm.watermark_scale_factor=125
vm.vfs_cache_pressure=200
vm.dirty_background_ratio=1
vm.dirty_ratio=5
# lz4, lzo-rle
#vm.page-cluster=1
# zstd
vm.page-cluster=0
```

Apply new changes:

```sh
sudo sysctl -p /etc/sysctl.d/99-vm-zram-parameters.conf
```
