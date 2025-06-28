# AWS EC2 Cheatsheet

<!-- tl;dr starts -->

The reason that I'm using AWS is because Cloudflare doesn't have compute engine service and its free tier counterpart is quite generous. I've decided to properly learn it.

<!-- tl;dr ends -->

## Table of Contents

- [Free Tier quotas](#free-tier-quotas)
- [Best practice](#best-practice)
- [Install FFmpeg inside AWS EC2 using Amazon Linux 2023](#install-ffmpeg-inside-aws-ec2-using-amazon-linux-2023)
- [IP address](#ip-address)
  - [Dynamic IPv4](#dynamic-ipv4)
  - [Static IPv4](#static-ipv4)

## Free Tier quotas

The tier type for AWS EC2 is 12 months. Be sure to migrate to a new account by next year.

| Resource               | t2.nano                | t3.nano                |
| ---------------------- | ---------------------- | ---------------------- |
| Region                 | All regions            | Same                   |
| Availability           | 750 hours/month        | Same                   |
| vCPU                   | 1                      | 2                      |
| RAM (GiB)              | 0.5                    | 1                      |
| CPU credits/hour       | 6                      | Same                   |
| Maximum CPU credits    | 144 (24 hours non-use) | 288 (48 hours non-use) |
| Egress                 | 100GB/month            | Same                   |
| Unlimited mode default | No                     | Yes (**TURN IT OFF**)  |
| Public IPv4            | 750 hours/month        | Same                   |
| Public IPv6            | Free (for now)         | Same                   |

## Best practice

Remove `ec2-user` from `sudo` list (you will need to ssh'ed into `root` account though):

```sh
# (optional) if you use Taiilscale, remember to give privilege to ec2-user first
sudo tailscale set --operator=ec2-user

sudo sed --in-place '/ec2-user ALL=(ALL) NOPASSWD:ALL/d' /etc/sudoers.d/90-cloud-init-users
```

## Install FFmpeg inside AWS EC2 using Amazon Linux 2023

```sh
# SSH into root user
docker exec -it tailscale tailscale ssh root@remotelab

# Install required dependencies
sudo yum install yasm nasm \
autoconf automake bzip2 bzip2-devel cmake freetype-devel \
gcc gcc-c++ git libtool make pkgconfig zlib-devel

# Download and extract FFmpeg source
curl -O -L https://ffmpeg.org/releases/ffmpeg-snapshot.tar.bz2 -C /tmp
tar xjvf /tmp/ffmpeg-snapshot.tar.bz2 -C /tmp
cd /tmp/ffmpeg

# Configure FFmpeg build
# Docs: https://gist.github.com/omegdadi/6904512c0a948225c81114b1c5acb875
./configure --prefix="$HOME/ffmpeg" \
  --bindir="$HOME/ffmpeg/bin" \
  --extra-cflags="-I$HOME/ffmpeg/include -fstack-protector-strong -fpie -pie -Wl,-z,relro,-z,now -D_FORTIFY_SOURCE=2" \
  --extra-ldflags="-L$HOME/ffmpeg/lib" \
  --extra-libs=-lpthread \
  --extra-libs=-lm \
  --enable-libfreetype \
  --disable-static \
  --enable-shared \
  --enable-rpath
  # --enable-gpl \
  # --enable-version3 \
  # --enable-nonfree
```

## IP address

By default, an AWS EC2 instance can have both static and dynamic IPv4 addresses:

### Dynamic IPv4

- Public: when you stop/start the instance, a new public IPv4 is newly assigned.
- Private: always assigned from the VPC subnet range and remains static within the VPC.

### Static IPv4

- Elastic IP (or EIP): set up a static public IPv4. Note that it's only free when it's associated with a running EC2 instance. If your EC2 is dead, make sure your Elastic IP shares the same fate.
- Private, static IP: You can assign a specific static private IP when launching the instance (?)
