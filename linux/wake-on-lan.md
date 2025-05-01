# Configure Wake-on-LAN on Fedora KDE 41

<!-- tl;dr starts -->

Before my older brother or me can buy a dedicated NAS, it's crucial to wake up my machine and turn on the Servarr stack remotely.

<!-- tl;dr ends -->

## 3 Prerequisites

### 1. The machine can only be woken up from ACPI S3 level, a.k.a Sleep, or Suspend on RAM.

### 2. Enabled Wake-on LAN on machine

There are numerous ways to check if your hardware supported Wake-on LAN:

- Go into BIOS/UEFI and check for anything that mentioned Wake-on LAN.

> NOTE: There isn't anything like that inside the BIOS/UEFI of Lenovo Yoga Slim 7 Pro - my laptop. I had to resolve to OS-level softwares.

- Wake-on Wireless LAN ("Wake-on WLAN" or "WoWLAN")

```sh
# Cre: chili555 (https://askubuntu.com/a/1333523/1689543)
# check Wake-on WLAN support
iw list | grep WoWLAN -A10
#
WoWLAN support:
  * wake up on disconnect
  * wake up on magic packet
  * wake up on pattern match, up to 20 patterns of 16-128 bytes,
    maximum packet offset 0 bytes
  * can do GTK rekeying
  * wake up on GTK rekey failure
  * wake up on EAP identity request
  * wake up on 4-way handshake
  * wake up on rfkill release
  * wake up on network detection, up to 8 match sets

# Cre: BeastOfCaerbannog (https://askubuntu.com/a/1439699/1689543)
# display wake-on wireless status on `phy0` device
# change `phy0` to your correspond device
iw phy0 wowlan show
#
WoWLAN is disabled

# enable WoWLAN for `phy0` device with magic packet
# (untested)
sudo iw phy0 wowlan enable magic-packet
```

3. Wake-on "Ethernet" LAN

```sh
# supported if there is a 'g'
sudo ethtool enp3s0f4u1u4 | grep -i 'supports wake-on'
#
# Supports Wake-on: pumbg

# check status
nmcli c show Ethernet | grep 'wake-on-lan:'
#
# 802-3-ethernet.wake-on-lan:             default

# enable Wake-on "Ethernet" LAN
nmcli c modify Ethernet 802-3-ethernet.wake-on-lan magic

# check status again
nmcli c show Ethernet | grep 'wake-on-lan:'
#
# 802-3-ethernet.wake-on-lan:             magic

# check status alternative
sudo ethtool enp3s0f4u1u4 | grep -i 'wake-on'
#
# Wake-on: g
```

### 3. Install a Wake-on LAN application on your Android/iOS device

I don't own an iPhone/iPad/i-whatever (and possibly never), there is only my trusty Redmi K20

I use **Shutdown Start Remote**, a very old application which isn't placed Google Play Store anymore, but there are plenty of similar applications out there.

Usually, the configuration requires your device's IP address and MAC address:

```sh
# get your network interface name
ifconfig
ip link show
nmcli device status

# my Ethernet network interface name
DEVICE_NAME=enp3s0f4u1u4

# IP address
ifconfig "$DEVICE_NAME" | grep 'inet '

# MAC address
ifconfig "$DEVICE_NAME" | grep -o -E '([[:xdigit:]]{1,2}:){5}[[:xdigit:]]{1,2}'
```

## Testing

Wake-on LAN mechanism involves sending a "magic" packet, more specific, a UDP datagram to the machine's port 9 via broadcast, or directly over Ethernet using EtherType 0x0842.

Run the following command to grab the relevant part of the payload for both wake-up methods, then trigger Wake Up from your application

```sh
# my Ethernet network interface name
DEVICE_NAME=enp3s0f4u1u4

# Cre: Alex Stragies https://superuser.com/a/1476401/2206521
sudo tcpdump -UlnXi "$DEVICE_NAME" ether proto 0x0842 or udp port 9 2>/dev/null | sed -nE 's/^.*20:  (ffff|.... ....) (..)(..) (..)(..) (..)(..).*$/\2:\3:\4:\5:\6:\7/p'
#
# f2:c1:5f:76:1c:ce
# f2:c1:5f:76:1c:ce
# f2:c1:5f:76:1c:ce
# f2:c1:5f:76:1c:ce
# ...
```

If the output is MAC address, your setup should be good.
