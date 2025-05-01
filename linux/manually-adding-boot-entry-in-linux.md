# Manually adding boot entry in Linux

<!-- tl;dr starts -->

After I reinstalled my BIOS, all boot entries are gone. Also during this time I also knew about how Windows updates can messed up EFI system partition, so I decided to separate them. Unfortunately my Fedora boot entry wasn't registered.

<!-- tl;dr ends -->

### Identify the EFI system partitions

```sh
sudo fdisk -l
```

### Toggle `boot` and `efi` flag on partition

```sh
# NOTE: Change the value to reflect your settings
DEVICE="/dev/nvme0n1"
PARTITION=1
sudo parted "$DEVICE" print

# run either command toggling both flags at the same time
sudo parted "$DEVICE" toggle "$PARTITION" boot
sudo parted "$DEVICE" toggle "$PARTITION" efi
```

### Add "Fedora" boot entry

```sh
# NOTE: Change the value to reflect your settings
DISK="/dev/nvme0n1"
PARTITION=1
LABEL="Fedora"
LOADER="\EFI\fedora\shimx64.efi"

sudo efibootmgr --create --disk "$DISK" --part "$PARTITION" --label "$LABEL" --loader "$LOADER"
```
