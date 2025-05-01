# Everything you need to know about WireGuard

<!-- tl;dr starts -->

WireGuard is a relative new _VPN protocol_ written by a consortium of Linux developers and cryptographers, designed to be simple, efficient, secure and avoid many pitfalls of other popular VPN protocols.

<!-- tl;dr ends -->

## Simplicity

Connection via exchanging public keys, like exchanging SSH keys. The rest is transparently handled by WireGuard like roaming between IP addresses (the ability to maintain connections when the device's IP address change).

## Security

- State-of-the-art cryptography that's being carefully selected by cryptographers.
- Small attack surface:
  - WG: 7k+ lines of code => reviewable by single individuals.
  - IPSec: 400k+ lines of code => code auditing is overwhelming task for large teams of security expert.

=> Less code, less chance of a vulnerability being present, stated by [Mullvad](https://mullvad.net/en/help/why-wireguard).

## Efficiency

High-speed cryptographic primitives + Lives inside Linux kernel (since version 5.6 in March 2020)

## In comparison with similar VPN protocols

- Faster, simpler, more useful than IPsec.
- More performant than OpenVPN.
