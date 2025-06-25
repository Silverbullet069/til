# OpenResty + Lua Cheatsheet

<!-- tl;dr starts -->

OpenResty + Lua is one of the most OP dynamic web platform that I've ever known.

<!-- tl;dr ends -->

## Overview

OpenResty is a web platform that integrates lots of components: Nginx, LuaJIT, Nginx C modules, Lua libraries, ...

To introduce dynamics into Nginx, when the tech came out in 2007, OpenResty version 1 chose Perl instead of Lua. This decision came from the technical preference of the author.

Soon, Perl's performance was far from meeting the requirements. OpenResty version 2 replaced Perl with Lua _partially_. Testing framework, Linter, CLI, ... are still written in Perl.

In OpenResty version 2, Engineers can write Lua script inside Nginx configuration file, allowing programmatically operations with the ability of processing high-concurrency, IO-bound tasks.

In order to integrate Lua into Nginx, OpenResty developed `lua-nginx-module`, an Nginx C module that embeds an enhanced fork of LuaJIT runtime environment that OpenResty team also maintained themselves.

OpenResty chose LuaJIT runtime environment over Standard Lua (POC-Rio Lua) because of its high-performance capability. LuaJIT runtime environment consists of 3 components:

1. Lua AOT Compiler source-to-bytecode
1. Lua interpreter, a.k.a LuaJIT VM, implemented in assembly.
1. Lua JIT Compiler, compiles frequently interpreted bytecode into native machien code during runtime.

> Similar to Java and CPython (>=v3.13).

OpenResty team also developed Lua `lua-resty-*` client drivers which facilitates the Lua integration with multiple services and various Nginx C modules (most of which are developed by the OpenResty team themselves). With them, engineers can implement API Gateway, soft WAF, caching, session management, ... therefore create a robust, high-performance, reliable, secure web application.

High performance + Dynamic = CDN. OpenResty is the technical standard of CDN.

> OpenResty was sponsored by Taobao before 2011 and supported by Cloudflare (my favorite major cloud provider) from 2012 to 2016.

## Use cases

This stack is very suitable for web application requiring **high-concurrency, IO-bound tasks**:

1. **Dynamic Web Portals:** end users (customers, employees) access their information and application services.
1. **API Gateway:** auth, rate-limit, request/response transformation, dynamic routing, ...
1. **Web Application Firewalls:** implement complex request inspection rules, store threat intelligence, IP reputation lists, ... in Redis.
1. **Session management:** store and retrieve user session data from Redis.
1. **Caching:** implement complex caching logic with Redis as the backend, control cache keys, TTLs, conditional caching and cache invalidation.

and many more...

**Q: How does using Nginx + Lua provide advantages over major cloud provider solutions (Cloudflare WAF and AWS WAF, AWS ALB/ELB and Cloudflare Load Balancing, AWS API Gateway, ...etc.)?**

**A:** While cloud provider solutions offer convenience and managed services, Nginx + Lua provides several distinct advantages:

1. **Cheap:** AWS services are expensive.

2. **Full control:** implement complex, business-specific logic that cloud solutions may not support: custom rate limit algorithms, request routing, security rules, ...

3. **Low latency:** processing requests at your edge or origin servers eliminates additional network hops to cloud provider services, reducing response times.

4. **Avoid Vendor Lock-in:** maintain portability across different cloud providers or on-premises infrastructure (Not really for AWS, it's the standard de-facto).

5. **Backend integration:** cloud providers sometimes don't support direct access to backend services (databases, ...) allows for more sophisticated request processing and data-driven decisions.

6. **High transparency:** full visibility into request processing, logging, and performance metrics without relying on cloud provider dashboards or APIs.

However, cloud solutions excel in areas like DDoS protection, global edge networks, and managed maintenance. The choice depends on your specific requirements for control, cost, performance, and operational complexity.

## Limitation

- **Not suitable for CPU-bound tasks:** complex math, video encoding, maching learning inference, ... are all tasks which do not create I/O bottleneck. Use other programming languages (C++, Go, Rust, Java, ... ) with mature ecosystem for fast CPU-intensive task processing is more appropriate.
- **Hard to scale and maintain complex business logic:** it's unwise to implement your intricate business logic entirely in Lua. It's like using C to do everything. Instead, use dedicated application framework (Python (Flask/Django), Java (Spring), ...).
- Hard to integrate with dependencies for which OpenResty hasn't developed a Lua client driver such as major cloud providers' services. Use other programming languages with SDK to them: Boto3 (AWS Python SDK), ...
- **Lack of prior expertise:** introducing Nginx + Lua + Redis learning curve is bad for project timeline.

## Technical aspects

### What is Synchronous?

Pseudo-code:

```lua
local res, err = query_mysql(sql)
local value, err = query_redis(key)
```

**Synchronous:** wait for MySQL query result to return before starting to query Redis.
**Asynchronous:** not waiting for MySQL query result to return and start querying Redis right away.

Most of OpenResty API are synchronous. only APIs related to background timers (e.g. `ngx.timer`) are asynchronous.

### What is Non-blocking?

What if it takes 1 seconds to query MySQL? The CPU, one of OS's resources, are idle and foolishly waiting for the return, wasting precious time which could be used to process requests from other connections.

Non-blocking is when it processes a IO-bound task such as querying database, the request is immediately yields so the Nginx Worker process can process requests from other connections.

ONE Nginx Worker process can handle from hundreds to tens of thousands of concurrent connections (C10K) to hundreds of thousands of concurrent connections (C100K) with minimal overhead per connection, depending on hardwares and softwares.

### What is Dynamics?

Nginx official release requires engineer to make modification on the configuration file on disk, and manually run CLI command to test its syntax and reload it. It doesn't have APIs to control runtime behavior.

Using Lua API provided in `lua-nginx-module`, modifying runtime behavior during runtime is do-able.

### OpenResty Architecture

[openresty architecture](./openresty-architecture.svg)

**Nginx Event-Driven Architecture:**

- OpenResty Worker processes are obtained by forking the Master process. The LuaJIT VM in the Master process is also forked.
- This LuaJIT VM is shared by all coroutines within the same Worker process.
- Lua code is run inside LuaJIT VM.
- Nginx Worker process calls `epoll` function, allow Worker process to monitor a large number of clients simultaneously for events (e.g. incoming data, a connection is ready to receive data from Nginx, ...)
- When an event occurs on a connection, the Worker process is notified and run the corresponding Lua coroutine to handle that specific request.
- If a Lua coroutine needs to perform a I/O blocking operation (e.g., reading from a database), it creates a Nginx subrequest to the external service, then yields control.
- This Nginx subrequest is made with Lua client driver `lua-resty-redis`, `lua-resty-mysql`.
- After Lua coroutine yielding, the Worker doesn't wait; it switches to processing another event or another ready coroutine for a different client connection.
- When the subrequest completes (database query finishes, HTTP request returns, etc.), Nginx's event loop resumes the yielded Lua coroutine to continue processing the original request.

=> At one point in time, each Worker process can only handle requests from one client, only one coroutine is running. Yielding coroutines allow multiple coroutines can be processed. A small number of worker processes can handle C10K, C100K.

![process](https://static.api7.ai/2022/10/13/634828bd1e4fe.png?imageMogr2/format/webp)

_Figure 1: The process behind Lua integration with Nginx Event-Driven Architecture (Source: api7.ai)_

**Q: What if Nginx used a thread-per-request model?**
A: Each connection would consume a separate thread, threads are extremly limited and would be depleted quickly under high load.

### Overview of [`lua-nginx-module`](https://github.com/openresty/lua-nginx-module)

Custom directives ([exhaustive list](https://github.com/openresty/lua-nginx-module?tab=readme-ov-file#directives)):

- `set_by_lua_[block|file] {}`: set variables
- `rewrite_by_lua_[block|file] {}`: forwarding, redirecting, ...
- `access_by_lua_[block|file] {}`: access, permissions, ...
- `content_by_lua_[block|file] {}`: generate return content.
- `header_filter_by_lua_[block|file]:` filter by response header, used with `proxy_pass`
- `body_filter_by_lua_[block|file]`: filter by response body, used with `proxy_pass`
- `log_by_lua_[block|file]`: logging

If the logic is simple. execute it all in `rewrite` or `content` phase is enough.

OpenResty's API has a list of contexts phases in which it can be executed, you will get an error if you use it out of scope.

<!-- TODO: finish your learning if you ever needed to use this stack -->

### Installation

1. OpenResty releases (recommended)

- Nginx core (OpenResty's optimized fork)
- [`lua-nginx-module`](https://github.com/openresty/lua-nginx-module) (or `nginx_lua`) developed by OpenResty.
- High quality Lua libraries (including `lua-resty-redis`) + Nginx modules + their transitive dependencies.

There aren't Docker build, self-building using [Alpine release](https://openresty.org/en/linux-packages.html#alpine) is an viable option.

For now, since I'm using EC2, I will use [Amazon Linux release](https://openresty.org/en/linux-packages.html#amazon-linux)

2. Self-build `nginx_lua` with Nginx (not recommended)

> Nginx, LucaJIT, OpenSSL official releases have limitations and long-standing bugs.

## References

- [Api7's "Getting Started with Lua"](https://api7.ai/learning-center/openresty/getting-started-with-lua)
- [Api7's "What makes OpenResty so special"](https://api7.ai/learning-center/openresty/openresty-getting-started)

<!-- TODO: finish reading the following articles -->

- [Api7's "OpenResty Is The Enhanced NGINX With Dynamic Requests and Responses"](https://api7.ai/learning-center/openresty/handling-requests-responses-dynamically)
- [Api7's "Tips for 10x Performance Improvement in OpenResty: `Table` Data Structure"](https://api7.ai/learning-center/openresty/tips-10x-performance-improvement-openresty-table-data-structure)
