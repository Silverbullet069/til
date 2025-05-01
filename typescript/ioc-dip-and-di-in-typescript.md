# IoC, DIP and DI In TypeScript

<!-- tl;dr starts -->

My personal projects all have wide scope for robust functionality. Learning OOP and SOP will help me in the run, but there is one concept that keeps bugging me all this time.

<!-- tl;dr ends -->

## Inversion of Control (IoC)

**IoC** is a broader **design pattern**, where the control flow is inverted from traditional programming:

- Traditional: Your code calls the framework's code.
- IoC: The framework's code calls your code

**IoC** answers the "what" question: invert control flow.

```ts
// Traditional
// You control when to call your code
function processOrder() {
  const data = readOrderData();
  validateOrder(data);
  saveOrder(data);
  sendConfirmation(data);
}
processOrder();

// IoC
// Framework controls when to call your code
class OrderProcessor implements FrameworkProcessor {
  processData(data: any) {
    // ...
  }
}
framework.registerProcessor(new OrderProcessor());
framework.start(); // framework controls when you call your code
```

## Dependency Injection (DI)

**DI** is a design pattern that implements IoC.

### What is dependency?

Dependency can be found both in the context of a function and a class.

```js
/**
 * Returns a random number within the specified range.
 * @param {number} min - The minimum value of the range
 * @param {number} max - The maximum value of the range
 * @param {function} random - A function that returns a random number between 0 and 1
 * @returns {number} A random number between min (inclusive) and max (exclusive)
 */
const getRandomInRange = (min: number, max: number): number =>
  Math.random() * (max - min) + min;
```

The functions depends on:

- 2 arguments: `min` and `max`
- 1 function: `Math.random()`, since `Math.random()` is not defined then `getRandomInRange()` won't work => `Math.random()` is a dependency.

What if we passed this function as an argument?

```js
/**
 * Returns a random number within the specified range.
 * @param {number} min - The minimum value of the range
 * @param {number} max - The maximum value of the range
 * @param {function} random - A function that returns a random number between 0 and 1
 * @returns {number} A random number between min (inclusive) and max (exclusive)
 */
const getRandomInRange2 = (
  min: number,
  max: number,
  random: () => number
): number => random() * (max - min) + min;

const result = getRandomInRange2(1, 10, Math.random);

const getRandomInRangeFinal = (
  min: number,
  max: number,
  random: () => number = Math.random
): number => random() * (max - min) + min;

const result2 = getRandomInRangeFinal(1, 10);
```

Another example, this time it's a counter that can increase, decrease and log its state.

```js
class Counter {
  state: number = 0;

  increase(): void {
    this.state += 1;
    // console is a dependency
    console.log(`State increased. Current state is ${this.state}.`);
  }

  decrease(): void {
    this.state -= 1;
    console.log(`State decreased. Current state is ${this.state}.`);
  }
}
```

The class just needs to be passed some object with the `log` method as dependency

```js
interface Logger {
  log(message: string): void;
}

class Counter {

  constructor(
    private logger: Logger,
  ) {}

  state: number = 0;

  increase(): void {
    this.state += 1;
    // console is a dependency
    console.log(`State increased. Current state is ${this.state}.`);
  }

  decrease(): void {
    this.state -= 1;
    console.log(`State decreased. Current state is ${this.state}.`);
  }
}

const counter = new Counter(console);
```

Replace `console` with another module that implements `Logger` interface:

```ts
const alertLogger: Logger = {
  log: (message: string) {
    alert(message);
  }
}

const counter = new Counter(alertLogger);
```

### Q: What's wrong with using `Math.random()` or `console` inside the function?

1. **Easy to test and debug**

Dependencies contribute most of the functionality. If something happened, it's very likely to be caused by one of the dependencies.

Dependencies can be injected with both concrete implementation and mock implementation, in case of WIP.

```js
const mockRandom = () => 0.1;
const result = getRandomInRangeFinal(0, 10, mockRandom);
console.log(result === 1);
```

2. **Scalability:** DI can inject new modules if they're the same as the old one.

```js
const otherRandom = (): number => {
  // ... another implementation of getting a random number
};
const result = getRandomInRangeFinal(0, 10, otherRandom);
```

### Automatic Injections and DI Containers

The injection is still manually done by 2 process: initialize the dependencies, and inject them into something else:

- Tedious
- Hard to maintain if there are a lot of concrete implementations for ONE interface, change in one place must reflect in all other places.
- Constructor arguments ordering mixing up

**DI Containers** can solve those problems. It's basically a module whose purpose is to provide dependencies to other modules.

- It knows which interfaces are required by which modules.
- It knows which concrete implementations associated with which interfaces.
- When creating modules that depend on such interfaces, it automatically initialize concrete implemenations and inject them into the modules and return the modules accordingly.

There are a lot of TypeScript libraries/framework that implements DI Containers. I chose [Brandi](https://brandi.js.org/getting-started) because of its simplicity in design. It only supports [Constructor Injection](https://en.wikipedia.org/wiki/Dependency_injection#Constructor_injection) and that's good enough for me.

```sh
npm install brandi
# or
yarn add brandi
```

```js
// logger.ts
export interface Logger {
  log(message: string): void;
}

export class ConsoleLogger implements Logger {
  log(message: string): void {
    console.log(message);
  }
}

// counter.ts
import { Logger } from './logger'

export class Counter {

  private state: number = 0;

  constructor(
    private logger: Logger
  ) { }

  increase(): void {
    this.state += 1;
    // console is a dependency
    this.logger.log(`State increased. Current state is ${this.state}.`);
  }

  decrease(): void {
    this.state -= 1;
    this.logger.log(`State decreased. Current state is ${this.state}.`);
  }
}

// tokens.ts
import { token } from 'brandi'

import { Logger } from './logger'
import { Counter } from './counter'

// token<T>() is a Brandi Pointer - a unique value that's used for relating entities
export const TOKENS = {
  logger: token<Logger>('logger'),
  counter: token<Counter>('counter')
};

// container.ts
import { injected, Container } from 'brandi'

import { ConsoleLogger } from './logger'
import { Counter } from './counter'
import { TOKENS } from './tokens'

// injected() is a Brandi Registrator - it registers a module with the tokens that refers to its dependencies
injected(Counter, TOKENS.logger);

export const container = new Container();

container
  .bind(TOKENS.logger)        // bind the token with
  .toInstance(ConsoleLogger)  // Binding Type - its concrete implementation
  .inTransientScope();        // Binding Scope - new instance will be created
                              // with each getting
container
  .bind(TOKENS.counter)
  .toInstance(Counter)
  .inTransientScope();

// index.ts
import { container } from './container'
import { TOKENS } from './tokens'

const counter = container.get(TOKENS.counter);
counter.increase();
counter.increase();
counter.decrease();
```

Here is the dependency flow diagram:

![dependency diagram](./dependency.svg)

Absolutely beautiful, nicely decoupled.

### DI Pros and cons

| Pros                      | Cons                                             |
| ------------------------- | ------------------------------------------------ |
| Write unit tests          | Complex, shallow learning curve                  |
| Relationship maintainance | Risk of vercomplexity                            |
| Scalability               | Compile time bug found on runtime                |
| Decoupling                | Hard to debug runtime bugs                       |
|                           | Autocompletion, find references, ... not working |

## Dependency Inversion Principle (DIP)

**DIP** is a **design principle**, the 'D' in SOLID, that states:

- High-level modules should not depend on low-level modules. Both should depend on abstractions.
- Abstractions should not depend on details. Details should depend on abstraction.

**My translation:** Classes depend on each other using interfaces or base classes (some languages doesn't support interfaces) instead of their concrete implementations.

**DIP** answers the "why" question: _abstraction is the key_.

```ts
// Bad
class OrderService {
  private mongoRepository = new MongoOrderRepository(); // Direct dependency

  placeOrder(order: Order) {
    this.mongoRepository.save(order);
  }
}

// Good
interface OrderRepository {
  save(order: Order): Promise<void>;
}

class MongoOrderRepository implements OrderRepository {
  async save(order: Order): Promise<void> {
    // ... MongoDB-specific implementation
  }
}

class OrderService {
  constructor(private orderRepository: OrderRepository) {} // Abstraction dependency

  placeOrder(order: Order) {
    this.orderRepository.save(order);
  }
}

const mongoOrderRepository = new MongoOrderRepository();
const orderService = new OrderService(mongoOrderRepository);
// even the initialization process of order repository is unrelated to order service
```

## References

- [Vladimir Lewandowski's " Dependency Injection in TypeScript "](https://dev.to/vovaspace/dependency-injection-in-typescript-4mbf)
- [6 Phút Để Hiểu Rõ Về Dependency Injection](https://codelearn.io/sharing/hieu-ro-ve-dependency-injection)
