# TypeScript Handbook

<!-- tl;dr starts -->

TypeScript is one of the two primary programming languages I am committed to mastering throughout my professional career in the technology industry.

<!-- tl;dr ends -->

## What's wrong with JavaScript?

- Unable to express the relationships between different units of code.
- Mismatching between language and program complexity made JS development a difficult task to manage at scale.
- Can't catch compiled errors:
  - Accessing unexisted variables/properties due to a simple typo.
  - Using equality operator `==`.
  - Forgetting API, leads to misuse.
  - ...

## TypeScript Overview

Its main purpose to be a _static type checker_ for JavaScript programs:

- Detecting errors in code without running it, is refered to as _static checking_.
- Determining what's an error and what's not based on the _kinds of value_ being operated on, is known as _static type checking_.

```ts
const obj = { width: 10, height: 15 };
const area = obj.width * obj.heigth; // typo!

// Property 'heigth' does not exist on type '{ width: number; height: number; }'. Did you mean 'height'?
```

Beyond its primary purpose as a static type checker, TypeScript significantly enhances the development experience through code completion, syntax highlighting, comprehensive documentation, ... in IDE/Code Editor.

## TypeScript Fundamentals

TypeScript is built on four core concepts that form the foundation of the language:

1. **Syntax**: TypeScript extends JavaScript's syntax while maintaining full compatibility
2. **Type System**: A robust static type system that validates code before execution
3. **Runtime Behavior**: Preserves JavaScript's runtime characteristics without modification
4. **Erased Types**: Types exist only during development and are removed during compilation

Understanding these fundamental principles provides the necessary context for effectively utilizing TypeScript in professional development environments.

### Syntax

TypeScript is a _superset_ language of JavaScript language. JavaScript syntax is legal TypeScript (but not the way around). Take any working JavaScript code and put it in a TypeScript file and it will run with no problem.

> **REMEMBER:** Syntax refers to the way we write text to form a program.

```ts
// Syntax errors

// ')' expected.
const a = (4

// Unterminated string literal.
const b = "Hello World
```

### Types

TypeScript is a _typed_ superset. The type checker is designed to allow correct programs through while still catching as many common errors as possible (how strictly it is can be configurable).

> **REMEMBER:** Types refers to rules about how different kinds of values can be used.

```ts
// Type error

console.log(4 / []);
// JavaScript: Infinity
// TypeScript: TypeError: The right-hand side of an arithmetic operation must be of type 'any', 'number', 'bigint' or an enum type.
```

### Runtime Behavior

TypeScript preserves the _runtime behavior_ of JavaScript and **never** changes it.

Take any working JS code and put it in a TS file, it's guaranteed to run the same way, even if TS found some type errors in the code.

By doing this, developers can easily transition between 2 language without breaking anything.

### Erased Types

TypeScript's compiler final output is a JavaScript file that contains compiled code _without_ the types.

No types also means TypeScript never changes the _runtime behavior_ of the program based on the types it inferred.

## TypeScript for JavaScript Programmers

### Types by Inference

_Definition:_ TypeScript generate types for a variable based on its assigned value. It offers a type-system without adding extra characters to make types explicit in your code.

_Example:_

```ts
let greeting = "Hello World";
// let greeting: string
```

### Defining Types

_Definition:_ There are a lot of design patterns to either explicitly or implicitly define types.

_Example:_

- Create an object with _inferred type_:

```ts
const user = {
  name: "Hayes",
  id: 0,
};

// name: string and id:number
```

- Describe object's shape using `interface` then declare a JS object conforms to the interface provided:

> **TIPS:** there are two syntaxes for building types: `interface` and `type`. Prefer using `interface` to using `type`, only use the latter when specific features are needed.

```ts
interface User {
  name: string;
  id: number;
} // no semicolon

const user: User = {
  name: "Hayes",
  id: 0,
};
```

- Error if an object doesn't match the interface:

```ts
const user: User = {
  username: "Hayes",
  // Object literal may only specify known properties, and 'username' does not exist in type 'User'.
  id: 0,
};
```

- Interface declaration with classes:

> Fact: JavaScript originally started as an object-oriented programming language (later become multi-paradigm when it supported functional programming).

```ts
interface User {
  name: string;
  id: number;
}

class UserAccount {
  name: string;
  id: string;

  constructor(name: string, id: number) {
    this.name = name;
    this.id = id;
  }
}

const user: User = new UserAccount("John Doe", 1);
```

- Use interface to annotate _parameters_ and _return values_ to functions:

```ts
function deleteUser(user: User) {
  // ...
}

function getAdminUser(): User {
  // ...
}
```

### Primitive types

- JavaScript primitive types: `boolean`, `number`, `string`, `null`, `undefined`, `bigint`, `symbol`.

- TypeScript primitive types:
  - `any`: allow anything
  - `unknown`: ensure someone using the type declares what the type is
  - `never`: it's not possible that this type could exist
  - `void`: a function which returns `undefined` or has no return value

### Composing Types

There are two popular ways to create complex types by combining simple ones: **Union** and **Generics**

#### 1. Union

_Definition:_ declare a type to be one of many types, using `|` symbol.

_Example:_

- Type and predication:

```
string 	typeof s === "string"
number 	typeof n === "number"
boolean 	typeof b === "boolean"
undefined 	typeof undefined === "undefined"
function 	typeof f === "function"
array 	Array.isArray(a)
```

- A man-made boolean:

```ts
type MyBoolean = true | false;
```

> **NOTE:** when hovering over `MyBoolean` in any IDEs/Code editors, you will see something like `type MyBoolean = boolean` which is a property of the Structural Type System.

- A set of `string` or `number` literals:

```ts
// plural form?
type WindowStates = "open" | "closed" | "minimized";
type LockStates = "locked" | "unlocked";
type PositiveOddNumbersUnderTen = 1 | 3 | 5 | 7 | 9;
```

- A function that takes both an array or a string:

```ts
function foo(bar: string | string[]) /* no return type here */ {
  // ...
}
```

**Q: Function Overloading or Union?**  
A: Both approaches are valid, each has its advatanges and caveat:

<!-- prettier-ignore -->
|Techinique|Union Types|Function Overloading|
|---|---|---|
|**Syntax Complexity**|Simple, concise|Verbose, requires separate gnatures|
|**Type Safety**|Good|Better|
|**Relationship between Behavior, Parameters and Return Types**|Same behavior for all parameter types, return type is inferred implicitly|Different behavior, different parameter type, different return types|
|**Return Type Precision**|Single implicit union return type for all parameter type|Specific return type for each parameter type|
|**API Documentation Conformity**|Less common|More common|
|**Extensibility**|Easy to add new types to Union|Requires adding new overload signatures|
|**Use case**|Internal implementation, simple functions|Public APIs, library interfaces|

```ts
// Complex Example Showing the Benefits of Overloading
// Cre: GitHub Copilot's Claude 3.7 Sonnet Thinking

// With union types (less precise)
function process(input: string | number | string[]) {
  if (typeof input === "string") {
    return input.length;
  } else if (Array.isArray(input)) {
    return input.join("");
  } else {
    return input.toString(16);
  }
}
// Return type is inferred as: number | string

// With function overloading (more precise)
function process(input: string): number;
function process(input: string[]): string;
function process(input: number): string;
function process(input: string | number | string[]): number | string {
  if (typeof input === "string") {
    return input.length;
  } else if (Array.isArray(input)) {
    return input.join("");
  } else {
    return input.toString(16);
  }
}
// Each call site gets the precise return type

const len = process("hello"); // Type: number
const joined = process(["a", "b"]); // Type: string
const hex = process(255); // Type: string
```

#### 2. Generics

_Definition:_ Provide variables to types.

A very common example is an array:

- An array without generics could contain anything.
- An array with generics can describe the values that the array contains.

_Example:_

```ts
interface Backpack<T> {
  add: (obj: T) => void;
  get: () => T:
}

// A shortcut, telling TS there is a constant called `backpack`
// Regardless of where it came from
declare const backpack: Backpack<string>;

// Obj is a string due to the declaration of get() method
const obj = backpack.get();

// `backpack`'s variable is registered as `string`, so this is invalid
backpack.add(1234); // Error: Argument of type 'number' is not assignable to parameter of type 'string'.
```

### Structural Type System

_Definition:_ One of TypeScript's core principles is that type checking focuses on the **shape** that values have. It's also known as _duck typing_ or _structural typing_.

- If two objects have the same **shape**, they are considered to be of the same **type**.

- There is no difference between how classes and objects conform to shapes.

_Examples:_

```ts
interface Point {
  x: number;
  y: number;
}

const logPoint = (p: Point) => {
  console.log(`${p.x}, ${p.y}`);
};

const point /* no explicit type declaration here */ = { x: 1, y: 1 };
console.log(point);
// Still run, output: "1, 1"
```

> **NOTE:** The shape matching only requires a **subset** of the object's fields/properties to match:

```ts
const point3 = { x: 1, y: 2, z: 3 };
logPoint(point3); // logs "1, 2"

const rect = { x: 1, y: 3, width: 10, height: 20 };
logPoint(rect); // logs "1, 3"

const color = { hex: "#ffffff" };
logPoint(color);
// Error: Argument of type '{ hex: string; }' is not assignable to parameter of type 'Point'. Type '{ hex: string; }' is missing the following properties from type 'Point': x, y

class VirtualPoint {
  x: number;
  y: number;

  constructor(x: number, y: number) {
    this.x = x;
    this.y = y;
  }
}

const newVPoint = new VirtualPoint(1, 2);
logPoint(newVPoint);
// Still run, output: "1, 2"
```

## TypeScript for Functional Programmers

### Built-in types

It's the same as [JavaScript built-in data structures](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Data_structures):
