# Click Application Development Practice

<!-- tl;dr starts -->

Click is the go-to CLI library for Simon when he has an idea that can be realized using a CLI application.

<!-- tl;dr ends -->

There are **SIX** practices that should be taken to heart.

## 1. Start with a template

Simon had developed his own Cookiecutter template for starting new ones, that template is [simonw/click-app](https://github.com/simonw/click-app). Use GitHub to create a new repository from that template.

By using GitHub Actions, he found a way to populate dynamic content into the newly create repository.

## 2. Enforce conventions on Arguments, Options

Click encourages a specific way of designing CLI tools.

Command have Arguments and Options.

1. **THREE** conventions on Arguments

- Arguments are positional - they are strings that passed directly into Command.
- Arguments can be required or optional.
- Commands can accept an unlimited number of arguments.

2. **SIX** conventions for Options

- Options are usually, optional.
- Options can be specified using single character version or long version.
  > E.g. `grep -i` is short for `grep --ignore-case`
- Options are occasionally required. Reading a Command that has so many positional arguments can be harder than reading one using 1 argument and multiple options for better separability.
- Options can be flags - they don't take additional paramaters. Simply being existed inside the Command switch something on.
  > E.g. `grep -i`, `grep -r`
- Options that are flags and appeared in their single character version can be combined.
  > E.g. `grep -ir` is short for `grep --ignore-case --recursive`.
- Options can take multiple parameters like Arguments.

3. Sub-commands: Children of Commands. Each sub-command can have their own family of commands.

   > E.g. `git add`, `git commit`, `git push`,... are all sub-commands of `git` command.

4. Help text: Every command and sub-commands should have `--help` option, the more detailed, the better.

## 3. Enforce consistency

As CLI tools scale, they end up with a growing number of commands, sub-commands, arguments and options.

_Pros and practices:_

- **Design Consistency:** New artifacts should be similar to existing artifacts. Also if you have multiple related CLI utilities, they must resemblance each other as well. Post an issue comment that says `similar to functionality in [TOOL]` with a copy of the `--help` output from that tool.
- **Get help from Generative AI**: Ask for design examples of existing CLI utilities that do something similar to your utility.

## 4. Versioning CLI interfaces like APIs

Practice Semantic Versioning (SemVer):

- Bump major version number on breacking changes.
- Bump minor version number on new features.
- Bump patch version number on bug fixes.

Simon said be cautious when making major changes. However, for inexperienced developers that haven't been exposed to a lot of different designs, making major changes is inevitable.

## 5. Include usage examples in --help

All of the tools have extensive online documentation, but for most of the times I need to look things up fast without opening a browser, a simple `--help` will do. More so, a `--help` with usage examples. Eventually we will forget how to use our own applications due to not having used it for a long time so usage examples are a significant help.

> **NOTE:** I used to say, your terminal history is your documentation.

The output of `--help` for [simonw/sqlite-utils's `convert` command](https://simonwillison.net/2023/Sep/30/cli-tools-python/#include-usage-examples-in---help).

## 6. Include --help in the online documentation

Larger tool tend to have extensive documentation independently of `--help` output. Both needs to be updated at the same time.

`--help` output can also live inside documentation site. Instead of copy-paste between code and docs, use [Cog](https://github.com/nedbat/cog) to automatically output `--help` option and embed into the docs.

## Reference

- [Simon Willison's Blog "Things I’ve learned about building CLI tools in Python"](https://simonwillison.net/2023/Sep/30/cli-tools-python/)
- [Cog](https://github.com/nedbat/cog)
