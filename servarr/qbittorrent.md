#

<!-- tl;dr starts -->

<!-- tl;dr ends -->

## FAQ

Q: Do I need port forwarding or UPnP to start downloading/uploading?
A: No, port forward/UPnP is for _incoming_ connection. _Outgoing_ connection are unrestricted by default in home network.

Q: Why I can only connect to a portion of seeders or unable to connect to any seeders at all?

A: Possible explanation:

- According to [Monkeyboy24 on Reddit](https://www.reddit.com/r/Piracy/comments/177fqc3/9_seeders_but_cant_connect_anyone_know_the_reason/k4sz056/), in the torrent swarm, there isn't a single peer that enabled port forwarding.

- Seeders stop seeding after finished downloading, but don't quit the torrent client. Same for unfinished torrents.

- Seeders limit the amount of upload speedj and upload slots, when those are taken by other peers, you simply unable to connect to them. This is typically true for public torrent swarm. [qBittorrent Forum #40360](https://forum.qbittorrent.org/viewtopic.php?p=40360#p40360)

- Peerblock, ISP blocking subnet, ...
