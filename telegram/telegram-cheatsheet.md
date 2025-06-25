# Telegram Cheatsheet

<!-- tl;dr starts -->

I documented every Telegram API I need to learn for my use cases.

<!-- tl;dr ends -->

## Route traffic to Telegram through Cloudflare Zero Trust

Add the following [CIDR subnets](https://core.telegram.org/resources/cidr.txt) and [domains](https://github.com/v2ray/domain-list-community/blob/master/data/telegram) to Cloudflare Zero Touch's Split Tunneling Include mode lists.

## Telegram Bot

First, set up a bot account with [@BotFather](https://telegram.me/botfather).

Each bot when it's created will be assigned a unique authentication token that can be used in part of the URI of Telegram Bot API.

E.g. `123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11`

Official Bot API endpoints are exposed by Telegram's existing infrastructure. I can abu... oops take advantage of that to create a temporary cloud storage solution.

In the near future, if I change to a self-hosted solution, I can use Local Bot API with less restrictive resources:

---

**Quotas:**

> This quota is retrieved at 2025-06-05. Check current quota at https://core.telegram.org/bots/features#local-bot-api

| API      | Max File Download | Max File Upload | Webhooks Protocol | Webhooks Port  | Webhooks Max Connections |
| -------- | ----------------- | --------------- | ----------------- | -------------- | ------------------------ |
| Official | 20MB              | 50MB            | HTTPS             | 443,80,88,8443 | 1-100                    |
| Local    | Unlimited         | 2000MB          | HTTP              | Any port       | 1-100000                 |

- Avoid sending 1 message/s in a chat.
- < 20 messages/s in a group.
- < 30 messages (bulk notifications)/s.

---

Telegram Bot API support:

- HTTPS request, in this form: `https://api.telegram.org/bot<token>/<method-name>`
- Method names are case-insensitive, so both `/methodname` or `/METHODNAME` will do.
- UTF-8 only.
- 2 HTTP methods: **GET** and **POST**
- 4 ways of passing parameters:
  - URL query string
  - `application/x-www-form-urlencoded` (simulate HTML form submissions, data encoded similar to URL query string)f
  - `application/json` (no uploading files) (best)
  - `multipart/form-data` (for uploading files)

HTTP Response Body: a JSON object

```json
// 2xx
{
  "ok": true,
  "description": "lorem ipsum dolar sit amet",
  "result": {
    // Depends on API endpoint's output
  }
}

// 4xx, 5xx
{
  "ok": false,
  "description": "explaining error...",
  "error_code": /* 4xx, 5xx */,
}
```

---

3 ways to send files:

1. If the file is already stored somewhere, you don't need to reupload it. Each file has a `file_id`, pass this `file_id` as a parameter instead of uploading. No limits imposed on files sent this way.

- Not possible to change file type when resending `file_id`
- Not possible to resend thumbnails.

2. Provide Telegram with HTTP URL. 5 MB/photo, 20 MB/other type.

- Ensure the MIME type is supported by API endpoint.
- `/sendDocument`: only worked with `.pdf` and `.zip`.

3. Post the file using `multipart/form-data`, 10MB/photo, 50MB/other type.

---

There aren't any way to fully automate the process of sending message to private chats, channels or groups and extracting `chat_id` from them beside using Telethon, but I'm afraid of being banned.

---

Don't promote another user an admin, it converts to a supergroup. Supergroup must be avoided to avoid being banned.
