# Why there are so many Python web frameworks?

<!-- tl;dr starts -->

I can name a few popular one in the market right now: Django, Flask, FastAPI, Sanic, ... but I didn't know why there are so many of them and when should I use which.

<!-- tl;dr ends -->

## TL;DR

<!-- prettier-ignore -->
|| Django | Flask | FastAPI | Sanic |
|---|:-:| :--: |:-:|:-:|
| **Architectural Pattern** | Monolithic | Microservice | Microservice | Microservice |
| **Calling Convention** | WSGI | WSGI (async support but not ASGI) | ASGI | ASGI |
