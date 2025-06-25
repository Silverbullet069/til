# Tailscale Learning

<!-- tl;dr starts -->

Sometimes I need to public some files inside my homelab into the wild but I don't want to touch firewall or open ports. I know Cloudflare Tunnel can solve this, but it has a shallow learning curve and my use case is far smaller that what it's capable of. Tailscale fits the description perfectly.

<!-- tl;dr ends -->

Tailscale is virtual private network (VPN) solution that allows all of your devices, independent of their physical networks or locations, to be on the same network. By doing so, device A can easily access device B, C, ... remotely as if they're on device A's network.

Tailscale use WireGuard, or more specifically, the userspace Go variant `wireguard-go` to create an extremely lightweight encrypted tunnels between devices (I use the term "devices", WireGuard uses "endpoints", Tailscale uses "node").

Tailscale operates as a "mesh VPN" instead of a traditional VPN.

---

In a traditional VPN, a "hub-and-spoke" architecture is used: multiple VPN clients connect to a centralize VPN gateway (or VPN concentrator) that redirect the traffic to multiple VPN servers. Both the gateway and the servers are managed by VPN providers.

![A traditional hub-and-spoke VPN.](https://cdn.sanity.io/images/w77i7m8x/production/3cbc3fa27f0b798d3a0bc98f57829a9083dad769-1400x1080.svg?w=3840&q=75&fit=clip&auto=format)

_Figure 1. A traditional hub-and-spoke VPN. Source: Tailscale Blog_

Before WireGuard, if the VPN concentrator is limited, and the only concentrator that you can connect is nowhere near the VPN clients, it incurs a high amount of latency. Furthermore, if the data center that host the remote resource is also nothere near this VPN concentrator, that's another high latency for you.

![Inefficient routing through a traditional VPN concentrator.](https://cdn.sanity.io/images/w77i7m8x/production/d0363ebfb736fa6e394aef3cb26585cecd842cd2-1320x980.svg?w=3840&q=75&fit=clip&auto=format)

_Figure 2(a). Inefficient routing through a traditional VPN concentrator. Source: Tailscale Blog_

However, WireGuard is different. You can create a multi-hub setup. Depending on your location and latency, the client can choose the best hub for you.

![A WireGuard multipoint VPN routes traffic more efficiently](https://cdn.sanity.io/images/w77i7m8x/production/66c858e17ca544818791e6d23e6085fa2e21b5e4-1320x980.svg?w=3840&q=75&fit=clip&auto=format)

_Figure 2(b). A WireGuard multipoint VPN routes traffic more efficiently. Source: Tailscale Blog_

Scability is a little tedious. Imagine, in a N + 5 nodes setup, there are N users and 5 servers.

- Each server stored 1 private key and (N users + 4 other datacenter) public keys.
- Each user stored 1 private key + 5 server public keys.
- When a new user is added, it advertises itself by distributing its public key to 5 existing servers.
- When a new server is added, it advertises itself by distributing its public key to N users + 5 existing servers.

Safe practices for key management is another thing you have to know.

---

In a mesh VPN, every device is called a "node". You can connect all the nodes to all the other nodes directly and securely using those extremely lightweight encrypted WireGuard tunnels.

![A Tailscale point-to-point mesh network minimizes latency](https://cdn.sanity.io/images/w77i7m8x/production/e989a4a69acd182abbd662d0de93cb31c4c4d210-1600x1080.svg?w=3840&q=75&fit=clip&auto=format)

_Figure 3: A Tailscale point-to-point mesh network minimizes latency. Source: Tailscale Blog_

How do they know each other? Tailscale devices who want to talk to each other, must talk to a coordination server first. It's a shared dropbox for that holds the public keys of ALL devices inside the a single Tailnet.

![Tailscale public keys and metadata are shared through a centralized coordination server](https://cdn.sanity.io/images/w77i7m8x/production/dbba97845c1ad1955669cc6a84c94f9d5fb78ade-1600x1080.svg?w=3840&q=75&fit=clip&auto=format)

_Figure 4: Tailscale public keys and metadata are shared through a centralized coordination server. Source: Tailscale Blog_

It's a hybrid centralized-distributed model.

- **The control plane is hub-and-spoke**, since it carries no traffic, just exchaning some keys. Here is how:

  - Each node generates a random keypair, associates the public key with its identity.
  - The node contact the coordination server, leaves its public key there + a note about where that node can be found, what domain it's in.
  - The node then downloads a list of public keys and addresses in its domain, which have been left on the coordination server by other nodes in the same Tailnet.
  - The node then configures its WireGuard instance with the appropriate set of public keys to connect to them.

  Wait, this mean Tailscale client have to trust anything that the coordination server give them? What if Tailscale secretly modified their coordination server to secretly populate a malicious public key to installed a node inside my Tailnet?
  => Tailscale introduces Tailnet Lock - a security feature where Tailscale node verify the public keys distributed by the coordination server before trusting them.

  - **NOTE:** the private key never leaves its node. Only node can encrypt packets addressed from itself and decrypt packets addressed to itself. This is a concept called "end-to-end encryption" or "zero trust networking".

- **The data plane is a mesh**.

---

Tailscale nodes must install Tailscale client software in order to connect to other nodes (with the exception of subnet routes).

Tailscale DOES NOT open any ports. Normally to public something into the Internet, you will have to "own" the firewall and punch some holes on it (i.e. port opening) but Tailscale saves you the trouble of configuring and being overthinking on the security of your set up by using a set of techniques to slide through the firewalls securely, such as NAT traversal ([read more](https://tailscale.com/blog/how-nat-traversal-works/)).

Tailscale clients within a Tailscale network (or Tailnet) using one of two types of connection:

Ideally, Tailscale create direct, P2P connections between all of the devices on the Tailscale network (or "Tailnet") and there is no Tailscale servers involved. This type of connection allows for lowest latency with highest throughput. I've managed to achieve this connection by enabling IPv6 on both devices.

Not ideally, direct connection can't be established (due to firewall policy, ...), it switched to a relay connection. More specific, a Tailscale server (Tailscale called them "DERP", or "Designated Encrypted Relay for Packets" server) is involved to relay the traffic between two devices.

![Relay servers in action](https://cdn.sanity.io/images/w77i7m8x/production/0e7f059799b6ba76cfc1df8e7c103d67620d8226-1320x900.svg?w=3840&q=75&fit=clip&auto=format)

What? Hub-and-spoke architecture in data plane now? Remember, private keys never leave node so DERP servers managed by Tailscale can't decrypt your traffic.

If your data isn't sensitive, with guarantee E2E encryption + Tailnet Lock, you don't have anything to worry about.

But if you're still overthinking, just self-host your coordination server and also DERP server but that's a bit too far and unnecessary in terms of security aspects (remember E2E?) by installing [Headscale](https://github.com/juanfont/headscale) on cloud providers' compute engine.

A Tailscale device can act as an [exit node](https://tailscale.com/kb/1103/exit-nodes), which acts as a gateway for the traffic of all devices that register this device as their exit node. You can say that device is similar to a VPN gateway.

Now comes the most robust feature of Tailscale: [Subnet Routers](https://tailscale.com/kb/1019/subnets). It can extend the Tailnet to include devices that don't or can't run the Tailscale client. Tailscale device which is a subnet router acts as a gateway between tailnet and physical subnets, enabling secure access from devices within one network to devices within other networks.

What if you have a local service that you want to temporarily expose it to public Internet? Use Tailscale Funnel. It lets you route traffic from public Internet to a local service running on a device in Tailnet, through Funnel relay servers.

## References

- [Comment on "Explain to me how TS works like I’m 5", Reddit, Ok-Gladiator-4924](https://www.reddit.com/r/Tailscale/comments/1asusnh/comment/kqsw9nn)
- [Comment on "Explain to me how TS works like I’m 5", Reddit, codeedog](https://www.reddit.com/r/Tailscale/comments/1asusnh/comment/kqtke7y/)
- [How Tailscale works, Tailscale Blog, Avery Pennarun, 2020-03-20](https://tailscale.com/blog/how-tailscale-works)
- [Tailnet Lock, Tailscale Blog, Tom D'Netto & Adrian Dewhurst, 2022-12-14](https://tailscale.com/blog/tailnet-lock)
- [Tailscale IPv6 support, Tailscale Docs, 2024-10-01](https://tailscale.com/kb/1121/ipv6)
- [IPv6 FAQ, Tailscale Docs](https://tailscale.com/kb/1134/ipv6-faq)
<!-- TODO: Learn how Tailscale adopts Zero Trust Networking architecture: https://tailscale.com/kb/1123/zero-trust -->
