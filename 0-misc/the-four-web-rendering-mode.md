# The Four Web Rendering Mode

<!-- tl;dr starts -->

Next time when you see React/NextJS/Nuxt/Django developers talking about how their tech stack is so robust, beautiful, the solution to ALL of the problems. Okay, React is just a tool (like many library/frameworks that use component-based design) to implement ONE rendering mode out of **FOUR** rendering modes and architectures.

<!-- tl;dr ends -->

## 1. Fully static sites, built from Static Site Generators (SSG)

- When end-users visit a _static site_, the server returns pre-built static assets (HTML, CSS, JS, images, videos, fonts, ...) right instantly. No dynamic rendering happens on the server while requesting.
- Static assets are generated at build-time and served directly from Cloudflare's CDN, making static sites fast and easily cacheable.
- Ideal for fully-static websites with content that rarely changes.

## 2. Single-Page Applications (SPAs) or Client Side Rendering (CSR):

- When end-users load an _SPA_, the server returns a minimal HTML shell and a JS bundle (served as static assets).
- From the JS bundle, the browser renders the UI client-side.
- After the initial load, all navigation occurs without full-page refreshes but via client-side routing (content changed via JS).
- Ideal for websites that need to be fast, app-like. Its content changed rapidly.

## 3. Server-Side Rendering (SSR):

- When end-users load an website that uses _SSR_, the server dynamically renders an HTML page on-demand for that request.
- Browser immediately displays the complete HTML instead of waiting for the JS code to run like CSR, resulting in a fast first page load.
- Once loaded, JS "hydrates" the page - content interaction via JS.
- Navigations can either, trigger new server-rendered pages, or server only constructed data and client fetched it and transition into CSR.
- Ideal for big, highly scalable enterprise-level web applications.

## 4. Mostly static, partially dynamic sites (also built from SSG):

- On a static page, end-users use dynamic functionality (e.g., searching, pagination, etc.), the content is dynamically constructed on the server, the browser fetches it via JS and renders it client-side.
- This is a new rendering mode that captures the benefits of static files (globally cached on the cloud's CDN, SEO-friendly, no JS needed, etc.) and client-side rendering (harness the computing resource from client's machine, ...).

## References

- ["Your frontend, backend, and database — now in one Cloudflare Worker", Korinne Alpers, 2025-04-08](https://blog.cloudflare.com/full-stack-development-on-cloudflare-workers/)
