# My Python toolkit

<!-- tl;dr starts -->

I would like to provide an overview on different Python tools.

<!-- tl;dr ends -->

## Language Servers

[Pylance](https://github.com/microsoft/pylance-release) is truly the MVP, supports bascially everything, note-worthy mentions: syntax highlighting, codecompletion, auto import, linting on change, docstring generator, ...

But, as a VSCodium user myself, I've to receive some bad news. As you might know (or not), VSCodium is the non-proprietary version of VSCode that eliminates telemetry integration. To protect their rightful benefits, Microsoft has make Pylance became useless if get installed inside VSCodium.

According to [VSCodium/vscodium/discussions#1641](https://github.com/VSCodium/vscodium/discussions/1641), the only viable workaround is to revert to version `2023.6.40`. Monitor the issues in [this StackOverflow thread](https://stackoverflow.com/q/75345501/9122512).

There are a few alternatives:

- [Jedi](https://github.com/pappasam/jedi-language-server)
- [Pyright](https://github.com/microsoft/pyright) (Pylance's core)
- [BasedPyright](https://github.com/detachhead/basedpyright/) (fork of Pyright)

Jedi is VSCode's default Python Language Server, its features are not wide as Pylance's but still it's enough. Sadly there is a bug that duplicates hints when hovering over artifacts. I've posted GitHub Issue [pappasam/jedi-language-server#331](https://github.com/pappasam/jedi-language-server/issues/331).

For Pyright, it's just a type checker. It doesn't have fancy features like syntax highlighting or autocompletions.

Finally, BasedPyright is the best gift that a Python developer and a FOSS user can receive, it's what I'm using right now. Syntax highlighting, autocompletion, ... you named it.

## Linters and Formatters

> formatters are linters that can auto edit.

- [autopep8](https://github.com/microsoft/vscode-autopep8)
- [flake8](https://flake8.pycqa.org/en/latest/) (Linter only)
- [Black](https://github.com/psf/black) (Formatter, use rules from flake8 linter)

## References

https://inventwithpython.com/blog/2022/11/19/python-linter-comparison-2022-pylint-vs-pyflakes-vs-flake8-vs-autopep8-vs-bandit-vs-prospector-vs-pylama-vs-pyroma-vs-black-vs-mypy-vs-radon-vs-mccabe/
