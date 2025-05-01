# Best practices when using Deno

<!-- tl;dr starts -->

When I was trying to crawl the Chinese version of Zombie World's chapters, I came across [eight04/ComicCrawler](https://github.com/eight04/ComicCrawler). I was astonished by the design of the tool. That's when I discovered Deno.

<!-- tl;dr ends -->

## Vendoring dependencies

Sometimes our dependencies aren't from `npm` or `yarn`, but from Deno third-party repositories. We need to import these dependencies with optimization in mind.

Let's use [`vm-server`](https://github.com/eight04/deno_vm/tree/master/deno_vm/vm-server) directory inside [eight04/deno_vm](https://github.com/eight04/deno_vm/) as an example.

Modules are imported via remote URLs:

```js
// index.js
import { TextLineStream } from "https://deno.land/std@0.203.0/streams/mod.ts";
import { VM } from "https://deno.land/x/worker_vm@v0.2.0/mod.ts";
```

Remote URLs are mapped to local files:

```json
// deno.json
{
  "importMap": "./vendor/import_map.json"
}

// vendor/import_map.json
{
  "imports": {
    "https://deno.land/": "./deno.land/"
  }
}
```

Dependencies are downloaded into the `vendor/deno.land` directory:

- `vendor/deno.land/std@0.203.0`
- `vendor/deno.land/worker_vm@v0.2.0`

This prevents network requests during execution while retaining remote URLs, facilitating offline development and enhancing performance.

> This approach is even better since I can replace these dependencies with unreleased versions that I create.
