# Cloudflare Workers

<!-- tl;dr starts -->

Cloudflare Workers is the serverless computing product for Cloudflare Developer Platform, similar to AWS Lambda.

<!-- tl;dr ends -->

> [!CAUTION]
>
> According to a [Cloudflare Blog written in 2025-04-08](https://blog.cloudflare.com/full-stack-development-on-cloudflare-workers/), Pages is deemed to be sunset in the future. All of the resources are poured into Workers. I don't know if by the time you're reading this TIL, Pages has been completely migrated to Workers. But from now on, you should ALWAYS start new project with Workers. Luckily I've known this news before I've started to learn Pages.

## What can you do with a Worker?

You can build a web application using:

- A single Worker returns a small HTML page on a single route under a single domain.
- A single Worker spans multiple domains, multiple routes for each domain,, different logic for each route.
- Multiple Workers that work together and deliver a single experience to end users.

Don't forget that Workers can integrate with other products in Cloudflare Developer Platform.

## Runtime

Workers runtime uses V8 engine, the same engine used by Chromium and Node.js. It's designed to be JS-standards compliant.

> If you're a JS/TS developer from the start, consider yourself lucky.

## Execution

Workers runtime runs in every data center of Cloudflare's global network. Every Worker run within its own "isolates". Cloudflare has designed the architecture for "isolate" that makes Workers efficient.

"Isolate" is a lightweight context that provide:

- Code
- Variables that code can access.
- A safe environment for code to be executed within.

One instance of the Worker runtime can run hundreds to thousands of "isolates", seamlessly switching between them.

Each isolate's memory is completely isolated, so each piece of code can be protected from other untrusted user-written code in the same runtime instance.

Isolates depend on containerization technology; therefore, an isolate can be created within an existing environment, resulting in very quick creation. If a virtual machine (VM) must be created for each function, we would have to wait for the VM's cold start to finish.

Workers pays the overhead of a JavaScript runtime ONCE on the start of a container.

Workers processes are able to run limitless scripts with no individual overhead.

An isolate can start ~100x faster than and consume an order of magnitude less memory than a Node process on a container or VM.

## Response flow

This is a very simple Workers flow:

```ts
export default {
  async fetch(request, env, ctx): Promise<Response> {
    return new Response("Hello World!");
  },
} satisfies ExportedHandler<Env>;
```

What happended behind the scenes is:

- A request to your `*.workers.dev` subdomain or to your Cloudflare-managed domain is received by any of Cloudflare's data centers.

- The request invokes the `fetch()` handler (more about Workers Handler later) defined in Workers code with the given request (there can be many Workers code inside your application but logically not all of them will match the request).

- Request is responded by returning a `Response` object.

## Static Assets

According to [my ultimate web tech stack](../0-misc/my-ultimate-web-tech-stack.md), I've chosen [11ty](https://github.com/11ty/eleventy) as my static site generator.

Sadly, by the time this TIL is written, [11ty wasn't supported by Cloudflare Workers](https://developers.cloudflare.com/workers/frameworks/), so I will use Workers to deploy the static assets that 11ty has built and develop the functions separately.

## References

- [Build applications with Cloudflare Workers (Learning Paths)](https://developers.cloudflare.com/learning-paths/workers/concepts/)
- [2025-04-08, Cloudflare Blog's "Your frontend, backend, and database — now in one Cloudflare Worker"](https://blog.cloudflare.com/full-stack-development-on-cloudflare-workers/)
