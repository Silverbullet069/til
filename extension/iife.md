# Immediately Invoked Function Expression (IIFE)

<!-- tl;dr starts -->

JavaScript developers may encounter the syntax pattern `(() => { ... })()`. This construct represents an **Immediately Invoked Function Expression (IIFE)**, a design pattern that executes a function immediately after its declaration.

<!-- tl;dr ends -->

Syntax:

```js
(() => {
  // ...
})();
```

Most of its advantages are derived from **security** concerns:

- **Avoiding global scope pollution:** By wrapping the entire script in an IIFE, all variables and functions defined within it are scoped to that function and don't pollute the global namespace. This prevents conflicts with other scripts on the webpage.

- **Content script isolation:** In the context of a browser extension content script, it runs in a shared JavaScript environment with the webpage. The IIFE creates a closure that protects the extension's internal variables and functions from being accessed or modified by the webpage's own scripts.

This is a standard pattern for browser extension content scripts because they need to run in the context of webpages while maintaining their own isolated execution environment.
