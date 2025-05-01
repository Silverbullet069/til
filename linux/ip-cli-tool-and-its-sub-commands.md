# `ip` tool and its sub-commands

<!-- tl;dr starts -->

Network configuration has always been seen as black magic, even among the tech workers.

<!-- tl;dr ends -->

## `iptables` / `ip6tables`

A CLI to interact with `netfilter`, a Linux kernel-based packet filtering framework. In order to do this, network administrators need to specify _rules_ to:

- Match packets based on certain criterias (protocol, src/dest IP, src/dest port, src/dest subnet, input/output interface, header, state...). They can be combined to create a complex matching system to differentiate packets from packets.
- Apply operations on the packets.

Its packet filtering mechanism is based on 3 components:

### Tables

```sh
-t, --table table
```

**1. `filter`**

- A packet can be either `-j ACCEPT`, `-j DROP` or `-j REJECT`
- If no `-t` option is specified, table value is `filter`.
- Support 3 chains: `INPUT`, `FORWARD`, `OUTPUT`.

```sh
# Allow SSH connections on port 22
iptables -t filter -A INPUT -p tcp --dport 22 -j ACCEPT
```

```sh
# Block incoming traffic from a specific IP
iptables -t filter -A INPUT -s 192.168.1.100 -j DROP
```

**2. `nat`**

- Network Address Translation, changing source/destination inside packets.
- Support 4 chains: `PREROUTING`, `INPUT`, `OUTPUT`, `POSTROUTING`.

```sh
# Redirect incoming traffic to internal web server

# Incoming Packet
#       v
# PREROUTING (nat)  <- [DNAT]
#       v
# Routing decision  -> `ip route`, `ip rule`
#       v
#    FORWARD
#       v
# POSTROUTING (nat) <- [MASQUERADE] / [SNAT]
#       v
# Outgoing Packet

iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.10:80

# [OPTIONAL]
# some system by default set DROP or REJECT policy for FORWARD chain
# traffic needs to be passing through your machine since it's acting as a router now
iptables -t filter -A FORWARD -p tcp --destination 192.168.1.10 --dport 80 -j ACCEPT
iptables -t filter -A FORWARD -m state --state ESTABLISHED,RELATED -j ACCEPT

iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE
```

```sh
# Load balancing
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.10:80
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.11:80 -m statistic --mode nth --packet 0
```

```sh
# Forward web traffic to internal web server
iptables -t nat -A PREROUTING -p tcp --dport 80 -j DNAT --to-destination 192.168.1.10:8080
```

```sh
# Redirect requests to another port
iptables -t nat -A PREROUTING -p tcp --dport 80 -j REDIRECT --to-port 8080
```

```sh
# Allows multiple devices on a internal/private network to share a single public IP address to access the internet
# Router have this rules by default
iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o eth0 -j MASQUERADE

# MASQUERADE and SNAT are used to change the source of packets
# -j MASQUERADE is used when router public IP of eth0 is dynamic (typical for home internet connections)
# -j SNAT (or source NAT) is preferred when static IP is utilized.
iptables -t nat -A POSTROUTING -s 192.168.1.0/24 -o eth0 -j SNAT --to-source 203.0.113.5 # router public IP
```

**3. `mangle`**

- Change packet's header.
- Support 5 chains: `PREROUTING`, `INPUT`, `OUTPUT`, `FORWARD`, `POSTROUTING`.

```sh
# Mark packets from specific source
iptables -t mangle -A PREROUTING -s 192.168.1.0/24 -j MARK --set-mark 1
```

```sh
# Set TTL value for outgoing packets
iptables -t mangle -A POSTROUTING -o eth0 -j TTL --ttl-set 64
```

**4. `raw`**

- Less common.
- Configure exemptions from connection tracking.

**5. `security`**

- Less common
- Used with SELinux to manage security contexts.

### Chains

**1. `INPUT`**

- Rules applied before packets went inside processes.
- Supported tables: `mangle`, `nat`

**2. `FORWARD`**

- Rules applied for packets that are routed through the current host.
- Supported tables: `mangle`, `filter`

**3. `OUTPUT`**

- Rules applied right after it's created from processes
- Supported tables: `mangle`, `nat`, `filter`, `raw`

**4. `PREROUTING`**

- Rules applied as soon as they come in network interfaces.
- Supported tables: `mangle`, `nat`, `raw`.

**5. `POSTROUTING`**

- Rules applied as they are about to go outside network interfaces.
- Supported tables: `magnel`, `nat`.

### Targets

A _target_ is an action that will be triggered after all matching criterias are met. There are two types of targets:

- Terminating targets: `DROP`, `ACCEPT`, `REJECT`.
- Non-terminating targets: `LOG`, ...

## `ip rule`

Analogy: "Traffic Director"

- Like receptionist directing people to different departments.
- Same as `iptables`, only more intuitive, network adminitrators create a set of _rules_ to determine **WHICH** routing table to use on packets that matched a set of criteria, such as src/dest IP, interface, mark, ...
- Multiple rules can match a packet, introduces the concept of "priority": the lower the number, the higher the priority. First matching rule is used.

```sh
# view all rules
ip rule show
ip rule list

# Default output usually looks like
# .
0:      from all lookup local       # local/broadcast address
32766:  from all lookup main        # most rules are inside here
32767:  from all lookup default     # empty

# Rule selectors
# Source-based
ip rule add from 192.168.1.0/24 lookup TABLE_NAME [priority] [NUMBER]

# Destination-based
ip rule add to 10.0.0.0/8 lookup TABLE_NAME [priority] [NUMBER]

# interface-based
ip rule add iif eth0 lookup TABLE_NAME [priority] [NUMBER]   # incoming
ip rule add oif eth0 lookup TABLE_NAME [priority] [NUMBER]   # outgoing

# firewall mark
ip rule add fwmark NUMBER lookup TABLE_NAME [priority] [NUMBER]
```

Troubleshooting:

```sh
ip rule show
ip route show table TABLE_NAME
ip route get DEST_IP from SRC_IP
```

Best practices:

- Keep rules minimal.
- Document the rules.
- Use meaningful table name.
- Consider table priority.
- Back up configuration: `ip rule show > rules.bak` and `ip route show > routes.bak`

## `ip route`

After knowing which routing table will be used for a specific packet, the _rules_ inside that table will decide _how that packet is handled_ and _where it will go_. `ip route` rule uses CIDR notation to indicate a particular packet destination.

Rules from `iptables` and `ip rule` has done a great job in matching the desired packets. but usually not all packets in a routing table are handled the same so you will need _rules_ for `ip route` as well. Its matching mechanism is very much the same as `iptables` and `ip rule`.

### Route selectors

```sh
# default route: applies this rule to all packets if none of other rules matched
# forward the packet to gateway 192.168.1.1
ip route add default via 192.168.1.1

# network route
# forward the packet to gateway 192.168.1.1 if destination IP matches 10.0.0.0/24 subnet
ip route add 10.0.0.0/24 via 192.168.1.1

# host route
# forward the packet to gateway 192.168.1.1 if destination IP matches 10.0.0.1/32
ip route add 10.0.0.1/32 via 192.168.1.1

# interface route
# delegate packet handling to network interfaces
ip route add 192.168.2.0/24 dev eth0
```

### Additional info

```sh
# multiple routing rules can be matched
# propose the "metric", the lower the number, the higher the priority
ip route add 10.0.0.0/24 via 192.168.1.1 metric 100

# if "table" option is not specified, it's added to table `main`
# best practice: policy-based routing, create a custom table with higher priorty than main
ip route add 10.0.0.0/24 via 192.168.1.1 table CUSTOM_TABLE

# protocols (not layer 3 tcp or layer 7 http))
ip route add 10.0.0.0/24 via 192.168.1.1 proto [static|kernel|dhcp|...]
```

ECMP (Equal-Cost Multi-Path, use for load-balancng):

```sh
ip route add default \
    nexthop via 192.168.1.1 dev eth0 weight 1 \
    nexthop via 192.168.2.1 dev eth1 weight 1
```

Different packets denied expression:

```sh
# blackhole route (drop packets)
ip route add blacklist 10.0.0.0/24

# unreachable route (return ICMP unreachable)
ip route add unreachable 10.0.0.0/24

# prohibit route (return ICMP prohibited)
ip route add prohibit 10.0.0.0/24
```

Troubleshooting:

```sh
# test routing decision
ip route get 8.8.8.8
ip route get 8.8.8.8 from 192.168.1.100
```

```sh
# show 'main' routing table
ip route
ip route show table main   # verbose

default via 10.65.0.1 dev wlan0 proto dhcp src 10.65.0.11 metric 305
# forward the packets to a gateway with address 10.65.0.1 if none of other rules match

10.33.0.0/16 dev vpn1 scope link
# forward the packets to network interface vpn1 if the destination matches 10.33.0.0/16

10.65.0.0/20 dev wlan0 proto dhcp scope link metric 305
# forward the packets to network interface wlan0 if the destination matches 10.65.0.0/20
# no gatewaysince the packets' destination is in the same network as the gateway, so the packets will be sent directly.
```

By default, as shown in `ip route`, there are 3 routing tables which are **local**, **main** and **default**, each table has an ID (**not priority**) and a name.

## `ip link`

View, modify, configure _network interfaces_ on system.

### CRUD operations

```sh
# display all network interfaces
ip link show

# bring an interface up/down
ip link set dev eth0 [up|down]

# Change MAC address, Maximum Transmission Unit (MTU), ...
ip link set dev eth0 address 00:11:22:33:44:55
ip link set dev eth0 mtu 1400

# Setup Virtual Interface...
```

## References

- [blogd's "`iptables`chuyên sâu"](https://blogd.net/linux/iptables-chuyen-sau/)
