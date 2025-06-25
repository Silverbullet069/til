# Terminology Differences

<!-- tl;dr starts -->

I've been focused on understanding the precise definitions of technological terminologies. To achieve this, I compare each term with its similar counterparts.

<!-- tl;dr ends -->

## [dietderpsy's comment on Reddit about the relationship between Program, Software and Application](https://www.reddit.com/r/learnprogramming/comments/kl785y/program_vs_software_vs_application/gh7cv37/)

- Hardware - The physical machine.
- Software - A program that runs on hardware.
- Program - A sequence of computing instructions. A piece of papar with code is a program. A code snippet on Visual Studio Code is a program. Where the entity lives doesn't determine whether it's a program, the program just refers to the instructions.
- Process - A program loaded into memory.
- Application - A program designed for the end user for a specific purpose. Some programs are general-purposed (like OS), or do not run for the end user.

## [Productivity vs Efficiency – What's the Difference?](https://trackingtime.co/productivity/productivity-vs-efficiency.html)

"Productivity" focuses on the **quantity of products**, concerns doing more within a specific timeframe. Overall, it describes how many items are produced.

"Efficiency" focuses on the **quantity of resources**, concerns doing the same amount of work (or more) using less time. Overall, it describes how well the resources are used.

## Interpreted vs Compiled Programming Languages: What's the Difference?

There are many debates about whether a programming language is compiled, interpreted, or both, and whether it uses an Ahead-of-Time (AOT) compiler, a Just-in-Time (JIT) compiler, or both. This can be particularly confusing with popular programming languages like Java, Python, and JavaScript.

**Compiler:** a program that converts a language into another language.

- Input: source code in a file, written in human-readable programming language.
- Output:
  - Code written in machine-readable language targeting a specific CPU architecture (e.g., AMD32, AMD64, ARM32, ARM64, RISC-V, ...) and a specific OS (GNU/Linux, Windows, MacOS, ...). The language can be called **instruction sets**. The instructions written in instruction sets are called **native machine code**.
  - Code written in machine-readable language targeting a specific virtual machine (e.g. JVM (JRE), PVM (CPython), LuaJIT VM ...). This "virtual machine" is also called a **bytecode/intermediate bytecode**. The virtual machine that _interprets_ bytecode is called **interpreter/bytecode interpreter**.

**Interpreter:** a program that executes instructions written in a machine-readable language that is independent of CPU architecture, OS, ...

**Ahead-Of-Time Compiler (or AOT Compiler):** A compiler type that create _both_ bytecode and native machine code **during compile time**.

Most of AOT compilers create native machine code.

Some AOT compilers create bytecode. AOT Compiler source-to-bytecode output has to be interpreted by a virtual machine, which means **the performance gain is from reducing loading time**.

E.g.

- C compiler: `.c` + `.h` => `.exe/.bin/...` (native machine code)
- Java AOT compiler (`javac`): `.java` => `.class` (bytecode)
- CPython AOT compiler: `.py` => `.pyc` (bytecode)

**Just-In-Time Compiler (or JIT Compiler):** A compiler type that creates native machine code **during runtime** from bytecode.

It is usually bundled with an interpreter. During runtime, the interpreter converts frequently executed bytecode into native machine code. **The performance gain is from reducing execution time.**

E.g.

- Java JIT compiler.
- PyPy JIT compiler.
- JavaScript JIT compiler.
- Official Python JIT compiler (from >=v3.13)

**Binary/machine code** and **bytecode** can exist in two forms:

- **Standalone files** for direct interaction:

  - Bytecode files: `.class` (Java), `.pyc` (Python), etc.
  - Machine code files: `.exe`, `.msi`, `.bin`, etc. ([exhaustive list](https://askubuntu.com/a/174356/1689543))

- **In-memory representation** ("internal bytecode") that isn't designed for direct interaction and only exists during script execution.

Here are the runtime environment's components of some popular programming languages:

1. Java: Java AOT Compiler source-to-bytecode + JVM + JIT Compiler.

1. CPython: AOT Compiler source-to-bytecode + PVM + JIT Compiler (only >=v3.13).

1. Standard Lua (PUC-Rio Lua): AOT Compiler source-to-bytecode + VM.

1. LuaJIT (alternative, high-performance implementation of Lua, targeting Lua 5.1): enhanced AOT Compiler source-to-bytecode + enhanced VM (implemented in assembly) + JIT Compiler.

<!-- prettier-ginore -->

| Criteria          | Compiled                                | Interpreted                            |
| ----------------- | --------------------------------------- | -------------------------------------- |
| Typing strategy   | Mostly static                           | All dynamic                            |
| Program size      | Larger (especially with static linking) | Smaller                                |
| Development cycle | Longer (compile-link-run)               | Shorter (immediate execution)          |
| Error detection   | Mostly at compile time                  | Mostly at runtime                      |
| Memory management | Often manual or compiled-in             | Usually automatic (garbage collection) |

## [Technique Vs Method Vs Methodology](https://anthroholic.com/distinction-between-technique-method-and-methodology)

### Technique

Key points:

- Lowest-level.
- Represent the practical procedures employed to perform specific tasks.
- Learn through practice and experience.
- Can be highly specialized depending on the field or task.

Examples:

- Dicing vegetables, kneading dough, or tempering chocolate are "cooking techniques"
- Interviews, surveys, statistical analyses are "sampling techniques" in a research context.

### Method

Key points:

- Mid-level.
- Methods are organized, systematic procedure used to achieve a goal or solve a problem.
- Methods consist of a series of steps, each step often makes use of specific _techniques_.
- Methods are designed to solve problems or achieve high-level goals.

Examples:

- The "Montessori method" encourages self-directed activity and hands-on learning.
- In research, the "scientific method" involves steps like: formulating a hypothesis, designing and conducting an experiment, analyzing data and drawing conclusions.

### Methodology

Key points:

- Highest-level.
- Methodology refers to the theoretical analysis of the "methods" applied in a field. This analysis can be seen as a "framework" that guides the selection, use and interpretation of the methods and techniques employed.
- Methodology explains the "why" behind the chosen methods and techniques.

Examples:

- In software development, Agile methodology is used for managing complex projects. It incorporates various methods like Scrum, Kanban, and techniques such as sprints or stand-ups.

### Real-world examples that encompass all 3 terminology

1. Education

Imagine an English teacher tasked with improving students' essay writing skills:

- Techniques can be writing bullet points, developing strong thesis statements, incorporating evidence to support an argument, ...
- Method can be a systematic approach, such as teaching each techniques one at a time, teaching can be introducing, practicing by providing examples as references for students and doing exercises. Finally, combine all techinques for a full essay writing assignment.
- Methodology can be "constructivist learning" (learner construct knowledge through experiences and social interaction, integrating new information with their own existing knowledge), which emphasizes active student participation and "learning by doing".

2. Business and software development

Your company wants to practice Agile methodology:

- Techniques within Agile include daily [stand-up meeting](https://en.wikipedia.org/wiki/Stand-up_meeting), retrospectives, pair programming, ...
- Methods within Agile are Scrum and Kanban, these are the methods that structure and organize the prior mentioned techniques to promote productivity and efficiency.
  > - "Productivity" focuses on the quantity of products, concerns doing more within a specific timeframe. Overall, it describes how many items are produced.
  > - "Efficiency" focuses on the quantity of resources, concerns doing the same amount of work (or more) using less time. Overall, it describes how well the resources are used.
- The Agile methodology, based on the Agile Manifesto, provides the theoretical framework that prioritizes high-level concepts such as individuals and interactions, working software, customer collaboration, responding to change.
