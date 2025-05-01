# File, Blob, MediaStream JS object

<!-- tl;dr starts -->

Understanding File, Blob and MediaStream will grant you great insight on how to crawl dynamic data from content providers.

<!-- tl;dr ends -->

## [Blob](https://developer.mozilla.org/en-US/docs/Web/API/Blob)

Blob (Binary Large Object) is a JavaScript file-like object of immutable, raw data.

Blob can read as:

- text: `const text = await blob.text(); // UTF-8 string`
- bytes: `const bytes = await blob.bytes(); // Uint8Array`
- stream: `const stream = blob.stream(); // ReadableStream`

### Blob URL / Object-URLs

Example:

```js
const obj = { hello: "World" };
const blob = new Blob([JSON.stringify(obj, null, 2)], {
  type: "application/json",
});
const objectURL = URL.createObjectURL(blob);
console.log(`Blob URL: ${objectURL}`);
// blob:nodedata:6cbc59e5-6c4f-4f3d-bd72-f47707509aaf

const text = await blob.text();
// { "hello": "World" }
```

Blob URLs ([W3C](https://w3c.github.io/FileAPI/#DefinitionOfScheme)) or Object-URLs ([MDN](https://developer.mozilla.org/en-US/docs/Web/API/URL/createObjectURL#Parameters) and method name) are used to reference Blob/File object which is currently , ephemeral content only lives inside browsers.

Blob URLs can only be generated internally by browser, used locally in single browser instance and in the same session:

```js
// Docs: https://developer.mozilla.org/en-US/docs/Web/API/URL/createObjectURL_static
// create a string containing a URL representing the object
// object: File, Blob, MediaSource
objectURL = URL.createObjectURL(object);

// release Blob/File obj
URL.revokeObjectURL(objectURL);
```

Blob URL/Object-URL is a _pseudo protocol_ to allow Blob/File JS objs to be used as URL source for images, download links for binary data. ... Rather than hotlink directly from server, content providers download content into local and create ephemeral content from it.

> Playing with browser's JS Debugger could find that downloaded content.

### Replacement for Data-URI

Blob URL/Object-URL is a better alternative to Data-URI, which are **strings encoded as Base64**. Its problem was that each char takes 2 bytes in JS, and 33% of data is added due to the Base64 encoding algorithm.

Blobs, on the other hand, are pure binary byte-arrays which doesn't have any significant overhead as Data-URI

**=> Smaller and faster during transmission.**
