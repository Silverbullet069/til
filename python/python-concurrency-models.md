# Python Concurrency Models

<!-- tl;dr starts -->

While trying to find the best way to maximize Apify free tier's resource utilization without touching its limit, I discovered 1 of 3 Python Concurrency Model: Asynchronous IO (short for "Async IO"). There are 3 different concurrency models in Python: Multiprocessing, Threading and Asynchronous IO.

<!-- tl;dr ends -->

## TL;DR

```d2
vars: {
  feature-font-size: 20
}

concurrency: "Python Concurrency Models" {
  style: {
    font-size: 32
  }
  asynchronous_io: "Asynchronous IO" {
    features: |md
      - IO-bound tasks.
      - Single process, single-threaded.
    | {
      style: {
        font-size: ${feature-font-size}
      }
    }
  }
  threading: "Threading" {
    features: |md
      - IO-bound tasks.
      - Single process, multi-threaded.
    | {
      style: {
        font-size: ${feature-font-size}
      }
    }
  }

  parallelism: "Parallelism" {
    multi_processing: "Multiprocessing" {
      features: |md
        - CPU-bound tasks.
        - Multiple processes.
      | {
        style: {
          font-size: ${feature-font-size}
        }
      }
    }
  }
}

legend: |md
  # Packages
  - `multiprocessing`
  - `threading`
  - `concurrent.futures`
  - `asyncio`
|

legend.style: {
  font-size: 24
}
```

![python concurrency model diagram](concurrency-model.svg)

- **Parallelism**: performing multiple operations at the same time.

- **Concurrency**: broader than _parallelism_, suggests that multiple tasks run in an overlapping manner. Concurrency does not imply parallelism, but the vice versa is true.

<!-- prettier-ignore -->
| **Concurrency models** | Multiprocessing | Threading | Asynchronous IO (Async IO) |
| ---------------------- | --------------- | --------- | -------------------------- |
| **CPU** | Many | One | One |
| **Multitasking Strategy** | Preemptive | Preemptive | Cooperative |
| **Switching Decision** | The processes all run at the same time on different processors (CPU cores) | The OS decides when to switch tasks that are external to Python | The tasks decide when to give up control |
| **Use Cases/Examples** | **CPU-bound tasks** (number-crunching, ...) | **IO-bound tasks** (file operations, database queries, ...) | **High-volume IO-bound tasks** (web servers handle 1000s of WebSocket connections, ...) |
| **Synchronization Coordinator** | IPC | Locks/Semaphore | No locks, required developers write non-blocking code |
| **Limitation by Global Interpreter Lock (GIL)** | No, each process run on its own Python Interpreter | Yes, threads are forced to run in sync mode, and No with *free threading* introduced since Python 3.13 | No, single-threaded |
| **Scalability Limitation** | Number of CPU cores | GIL (suitable for few threads) | All awaited tasks are long-running ones |
| **Code Complexity** | **High** (IPC, memory separation, ...) | **Moderate** (race condition, OS-level management, GIL limitation...) | **Low/Moderate** (non-blocking code required) |
| **Package** | `multiprocessing` (low-level), `concurrent.futures` (high-level) | `threading` (low-level), `concurrent.futures` (high-level) | `asyncio` |
| **Performance Optimization** | Avoids GIL, uses as much cores as possible | Only blocking libraries are available | Non-blocking libraries are available as well |
| **General** | **Multiple system processes** run multiple ToTs at the same time | **Single process**, **multiple threads** can only run 1 ToT, but cleverly take turns to speed up the overall process | **Single process**, **single-threaded** can only run 1 ToT, but cleverly take turns to speed up the overall process |

## Introduction: What is Concurrency?

Dictionary definition: **simultaneous occurrence**. So, what are the things that are "occuring simultaneously"?

- Process
- Thread
- Task

At a high-level, they're the same and all refers to "a sequence of instructions that run in order".

**Analogy**: a series of **trains of thought** (now refers to as ToT). Each one can be stopped at certain points, the brain can switch to a different one. The state of each train is saved so it can be restored where it was interrupted.

But at a much lower-level, they represent slightly different things:

- Process: a collection of resources including memory, file descriptors, ... that's unshareable between other processes (that's why Inter-Process Communication (IPC) existed). Overall, a completely different program.
  - In Python context, each process runs in its own Python Interpreter.
  - Each ToT can run on a separated CPU core.

## Multitasking strategies

- **Preemptive Multitasking:** OS-level management, OS knows about each process/thread and interrupts it _at any time_ to start calling a different process/thread.
  - Both easy and hard, depends on whether or not the code need to implement context switch from just a trivial `x = x + 1`.
- **Cooperative Multitasking:** No OS-level management. Tasks cooperate with each other by announcing when they're ready to be switched out:
  - Much easier to implement than Preemptive Multitasking. Know where task will be swapped out => Easier to read the execution flow.

## 2 problems that Concurrency addresses

- IO-bound: cause program to slowdown because it needs to wait for input or output from external resource, things that are much slower than CPU. E.g. File system, Network connection, ...

![io bound diagram](https://files.realpython.com/media/IOBound.4810a888b457.png)

=> Solution: overlap the times spend waiting by doing something else in the meantime.

- CPU-bound: the resource limiting the speed of the program is the CPU.

![cpu bound diagram](https://files.realpython.com/media/CPUBound.d2d32cb2626c.png)

=> Solution: do more computations in the same amount of time.

## Python Concurrency Models

### Multiprocessing

Utilizes 2 Python packages: `concurrent.futures` (high-level) and `threading` (low-level).

```py
threading.local() #
```

### Threading

### Asynchronous IO (Async IO)

## References

- [Brad Solomon's "Async IO in Python: A Complete Walkthrough", 2019-01-16, RealPython](https://realpython.com/async-io-python/#a-full-program-asynchronous-requests)
- [Jim Anderson's "Speed Up Your Python Program With Concurrency", 2024-11-25, RealPython](https://realpython.com/python-concurrency/)
