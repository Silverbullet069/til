# Telegram Overview

<!-- tl;dr starts -->

Telegram is banned in my country, but that doesn't stop me from using this fantastic platform.

<!-- tl;dr ends -->

_Definition:_ According to [Bots: An introduction for developers](https://core.telegram.org/bots):

```md
Bots are **small applications** that run entirely within the Telegram app. Users interact with bots through **flexible interfaces** that can support **any kind of task or service**.
```

Basically, you chat with it according to its rules, and it sprung up output for you.

Here are some use cases:

- Replace normal websites.
- User auto-reply.
- Sell physical/digital products via Telegram Stars.
- Create a dedicated tool (e.g. image resize, weather forecast, ...)
- Leverage existing groups/channels by adding a bot into them.
- Integrate with 3rd-party services, APIs, devices to instantly process and update information (e.g. allow Location permission to generate weather forecast)
- Host games.
- Build social networks.
- Sell tech solutions via a robust ecosystem of monetization features.

Telegram Group vs Telegram Channel:

<!-- prettier-ignore -->
| Feature | Telegram Group | Telegram Channel |
| --- | --- | --- |
| Data model (relationship) | N-to-N communication | 1-to-N communication |
| Who can post? | All members can send messages, Admin can restrict this | Only admins (owner and designators) can post |
| Maximum no. of participants  | 200k+ members | Unlimited subscribers |
| Message Sender | Messages show the name of the individual sender | Posts are signed with the channel's name (Admin signatures if enabled can show which admin posted) |
| History message visibility | Admins can configure if new members see older messages or not | New subscribers can always see the entire message history |
| Comments | The group itself is for discussions | Linked groups for comments on posts |
| Public/Private | Can be public or private (via invite link) | Same as Group |
| Admin Roles | Granular permissions for multiple admins | Same as Group |
| Use Cases | Team chats, community discussions, friends and family | News, official announcements, content feeds, blogs, ... |
