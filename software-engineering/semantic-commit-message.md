# Semantic Commit Message

<!-- tl;dr starts -->

There are 2 subjects regarding the practice of writing a good commit messages: Semantic Versioning (SemVer), Conventional Commits (extended with Angular convention).

<!-- tl;dr ends -->

## Semantic Versioning (SemVer)

_Definition:_ Given the version number `MAJOR.MINOR.PATCH`, increment the:

- `MAJOR` version when you make incompatible API changes.
- `MINOR` version when you add functionality in a backward compatible manner.
- `PATCH` version when you make backward compatible bug fixes.

## Conventional Commits

_Definition:_ Conventional Commits specification is a lightweight, easy to implement convention on top of commit messages. More specifically, it provides an easy set of rules when creating commit messages. Angular introduces its Commit Message Guidelines that provide much more details than Conventional Commits specification.

_Examples:_

```txt
docs: correct spelling of CHANGELOG
=======================================================================
feat(lang): add Polish language
=======================================================================
feat!: send an email to the customer when a product is shipped
=======================================================================
feat: allow provided config object to extend other configs

BREAKING CHANGE: `extends` key in config file is now used for extending other config files
=======================================================================
chore!: drop support for Node 6

BREAKING CHANGE: use JavaScript features not available in Node 6.
=======================================================================
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
=======================================================================
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue but are
obsolete now.

Reviewed-by: Z
Refs: #123
```

### Structure

```txt
<type>[(scope)]: <description>

[optional body]

[optional footer(s)]
```

### Types

_Definition:_ One noun that indicates the subject of the changes.

- `<type>!:` introduce a breaking API change, correlates with `MAJOR` in Semantic Versioning.
- `feat:` introduce a feature, correlates with `MINOR` in Semantic Versioning.
- `fix:` patches a bug, correlates with `PATCH` in Semantic Versioning.
- `build:` (Angular) changes that affect the build system or external dependencies.
- `ci:` (Angular) changes to CI configuration files and scripts
- `pref:` (Angular) changes that improve performance.
- `refactor:`(Angular) changes that neither fixes a bug nor adds a feature.
- `style:` (Angular) changes that do not affect the meaning of the code (whitespace, formatting, ...)
- `test:` (Angular) add missing tests or correcting existing tests.
- `revert:` (Angular) revert a previous commit. Footer refs the commit SHAs that are being revered

### Scope

_Definition_: The name of the dependency affected. Scope benefits the most if you're developing and maintaining for a framework that consists of multiple libraries/packages.

### Description

_Definition_: One succint sentence:

- Use the verb that is in imperative, present tense. E.g. `change`. Not `changed` or `changes`.
- Don't capitalize the first letter. E.g. `chore: initial release`, not `chore: Initial release`
- No full stop. E.g. `chore: initial release`, not `chore: Initial release.`

### Body

_Definition:_ Additional information about the description. Use the same rule set as [Description](#description).

### Footer

_Definition:_ Contains any information about `BREAKING CHANGES:` and also the place to `refs` or `closes` Github Issue that's related to the commit.

## Reference

- [Samuel-Zacharie Faure's "How atomic Git commits dramatically increased my productivity - and will increase yours too"](https://dev.to/samuelfaure/how-atomic-git-commits-dramatically-increased-my-productivity-and-will-increase-yours-too-4a84)
- [Semantic Versioning 2.0.0](https://semver.org)
