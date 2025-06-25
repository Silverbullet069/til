# Semantic Commit Message

<!-- tl;dr starts -->

There are 2 subjects regarding the practice of writing a good commit messages: Semantic Versioning (SemVer) and Conventional Commits.

<!-- tl;dr ends -->

## Semantic Versioning (SemVer)

_Definition:_ Given the version number `MAJOR.MINOR.PATCH`, increment the:

- `MAJOR` version when you make incompatible API changes.
- `MINOR` version when you add functionality in a backward compatible manner.
- `PATCH` version when you make backward compatible bug fixes.

## Conventional Commits

```txt
<type>(<scope>): <description>
<BLANK LINE>
<body>
<BLANK LINE>
<footer>
```

Each commit message consists of a **header**, a **body** and a **footer**.

The header includes a **type**, an optional **scope** and a **description**.

### Type

A single noun indicating the subject of the change. Must be one of the following:

- `<type>!:` exclamation mark or `BREAKING CHANGE:` footer introduce a breaking API change. Correlates with `MAJOR` in Semantic Versioning.

  > Refrain from using this type, introducing breaking changes means users have to acknowledge the change and proceed in migrating process to make existing infrastructure reflect them.

  ```
  feat!: send an email to the customer when a product is shipped
  ```

  ```
  feat: allow provided config object to extend other configs

  BREAKING CHANGE: `extends` key in config file is now used for extending other config files
  ```

  ```
  chore!: drop support for Node 6

  BREAKING CHANGE: use JavaScript features not available in Node 6.
  ```

- `feat:` introduce a feature for the user (not a new feature for build script). Correlates with `MINOR` in Semantic Versioning.
- `fix:` patches a bug (again, not a bug in build script). Correlates with `PATCH` in Semantic Versioning.
- `test:` add new tests for new features, change old tests to fix regression tests not working, add missing tests or correcting existing tests.
- `docs:` change to the documentation.
- `chore:` anything that doesn't change the state of the codebase. E.g. renaming a variable/function/class, formatting the code, fixing missing semicolons, removing whitespaces/tabs ...

Here are some Angular-specific types:

- `build:` (Angular) changes that affect the build system or external dependencies.
- `ci:` (Angular) changes to CI configuration files and scripts
- `pref:` (Angular) changes that improve performance.
- `refactor:` (Angular) rename variables, deduplicate codes, ...
- `style:` (Angular) formatting, remove whitespace, ...
- `revert:` (Angular) revert a previous commit. The commit SHAs that are being revered should be included in footers.

```
revert: let us never again speak of the noodle incident

Refs: 676104e, a215868
```

> IMO, `style:` + `refactor:` seems overlapping each other and `chore:` as well.

```
docs: correct spelling of CHANGELOG
```

### Scope

The name of the dependency affected if you're developing and maintaining for a framework that consists of multiple libraries/packages. If you're developing a zero/few dependencies project, you can ignore scope.

```
feat(lang): add Vietnamese language
```

### Description

One succint sentence:

- written in imperative mood (i.e. verb in present tense, no pronoun)
- no capitalize the first letter
- no full stop.
- refs, closes to issues, bugzilla tickets (if any)

> Angular convention said that you can put it in **footer**, but again I want to see the issue number in Web UI.

**NOTE:** Each line in a commit message should not exceed 80/100 characters since it allows the message to be easier to read on GitHub and various git tools.

> I've seen long commit messages hidden on Web UI.

````
chore: initial release    # good
chore: Initial release.   # bad

feat: add ```--no-colour``` option, closes #1    # good
feat: added ```--no-colour``` option, closes #1  # bad
````

### Body and Footer

A full-fledge commit message:

```
fix: prevent racing of requests

Introduce a request id and a reference to latest request. Dismiss
incoming responses other than from latest request.

Remove timeouts which were used to mitigate the racing issue but are
obsolete now.

Reviewed-by: Z
Refs: #123
```

### Tips

You should use a commit message linter, such as [conventional-changelog/commitlint](https://github.com/conventional-changelog/commitlint) to force you (and your team members) to write conventional commit messages.

Keeping the commit messages following conventional can allow you to automatically generate beautiful changelog and release note.

## Reference

- [Samuel-Zacharie Faure's "How atomic Git commits dramatically increased my productivity - and will increase yours too"](https://dev.to/samuelfaure/how-atomic-git-commits-dramatically-increased-my-productivity-and-will-increase-yours-too-4a84)
- [Semantic Versioning 2.0.0](https://semver.org)
- [joshbuchea/semantic-commit-messages.md](https://gist.github.com/joshbuchea/6f47e86d2510bce28f8e7f42ae84c716)
