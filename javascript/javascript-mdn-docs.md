# Javascript Mdn Docs

<!-- tl;dr starts -->

**TL;DR:**

<!-- tl;dr ends -->

<!-- TODO: finish this -->

## JavaScript Data Types

### Dynamic programming language with dynamic types

Variables in JS aren't directly associated with any concrete type, they can be assigned and re-assigned with values of all types.

```js
let foo = 1; // number
foo = "bar"; // string
foo = true; // boolean
```

### Weakly typed language

JavaScript allows _implicit type conversion_ (or _coersion_) when an operation involves mismatched types, instead of throwing type errors.

```js
const foo = 1; // number
foo = 1 + "1"; // NOT AN ERROR! Instead, JavaScript coerces `foo` to a string, so it can be concatenated
console.log(foo); // 11
```

> **NOTE**: Not supported for Symbol and BigInt types.

### Primitive values

All types except Object define

**Refresh memory:** JavaScript has 8 built-in types:

- `Number`: a double-precision IEEE 754 floating point.
- `String`: an immutable UTF-16 string.
- `BigInt`: integers in the arbitrary precision format.
- `Boolean`: `true` and `false`.
- `Symbol`: a unique value usually used as a key of an Object property.
- `Null`:

<!-- prettier-ignore -->
|Type|Global function|`typeof` return value|
|---|---|---|
|**Null**|`N/A`|`object`|
|**Undefined**|`N/A`|`undefined`|
|**Boolean**|`Boolean()`|`boolean`|
|**Number**|`Number()`|`number`|
|**BigInt**|`BigInt()`|`bigint`|
|**String**|`String()`|`string`|

- Global function: used for explicity [type casting](https://developer.mozilla.org/en-US/docs/Glossary/Type_Conversion). It has the same effect as using `!!`.
- `new` keyword: ES6 introduces [Classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes) to JavaScript taking the best parts of _prototypal inheritance_ and common patterns. Part of that is the `new` keyword, it's basically calling the constructor of the class, the result will be a _wrapper object_

```js
class Foo {
  constructor() {
    // ...
  }
}

Foo();
// Runtime error: throws
// Compile error (TypeScript): class constructors must be invoked with `new`.
```

arbitrary properties can be assigned to the object. This isn't feasible for primitive values as they can't hold properties.

> **NOTE:** `new` keyword is considered bad practice for `Boolean` since its `typeof` will always be `object`, something like `new Boolean(0)` is always truthy.

## Reference

- [MDN Web Docs's "JavaScript data types and data structures"](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Data_structures)
