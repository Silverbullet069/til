# GitHub Copilot Chat best practices

<!-- tl;dr starts -->

GitHub Pro gave me a GitHub Copilot plan for free and I've been using it ever since.

<!-- tl;dr ends -->

## Service interfaces

1. [Web-based UI](https://github.com/copilot)
2. [VSCode Extension](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)

> [!NOTE]
>
> GitHub Copilot and GitHub Copilot **Chat** are two different extenscions, the latter depends on the former.

## Prompt engineering features

There are multiple ways that users can specify their "custom instructions" (Cursor called "rules):

<!-- prettier-ignore -->
| Feature | Characteristics | Location and Scope | Activation | Per-language |
| --- | --- | --- | --- |
| Extension settings | Simple, one-size-fit-all, arbitrary | `.vscode/settings.json` (workspace)<br/>`.config/VSCodium/User/settings.json` (user)| Automatic | Yes |
| Instructions file | Structured, standardized | `.github/instructions/*.md` (workspace)<br/>`.config/VSCodium/User/prompts/*.md` (why `prompt` directory) (user) | Automatic | Yes |
| Prompt file (latest) | Simple, ad-hoc, reusable | `.github/prompts/*.md` (workspace)<br/>`.config/VSCodium/User/prompts/*.md` (user) | Manual | No |

### [Custom instructions specified in Extension settings](https://code.visualstudio.com/docs/copilot/copilot-customization#_use-settings)

1. **Code generation**: `Always add a comment`, `In TypeScript always use underscore for private field names.`, `Always use React functional components.`, ...
1. **Test generation**: `Always use vitest for testing React components.`, `Implement rate limiting and throttling.`, `Implement logging and monitoring for security events.`, ...
1. **Code review**: `Ensure all endpoints are protected by authentication and authorization.`, `Validate all user inputs and sanitize data.`, ...
1. **Commit message generation**: [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/)
1. **PR title + description generation**: `Include every commit message in the pull request description.`

> [!IMPORTANT]
>
> I still don't know in which condition do these custom instructions get referenced. Best to monitor the `Used X reference` panel.

## [Context (until 2025-06-13)](https://code.visualstudio.com/docs/copilot/chat/copilot-chat-context)

There are multiple types of context:

- `@chat-participant` or `@chat-participant /command`.
- `#chat-variable`
- `Files & Folders`
- `Instructions`
- `Problems`
- `Tools`

> **NOTE:** You can see that there are a lot of overlap in feature. The GitHub Copilot Chat extension is actively under development so major breaking changes may be introduced in the future.

## Indexing

There are three types of indexes, ordered from least to most robust:

- **Basic index**
- **Local index**
- **Remote index**.

Logic:

- If your project has **<750** indexable files, local index is built **automatically**.
- If your project has **750-2500** indexable files, local index must be built **manually** (via `Ctrl + Shift + P` -> `GitHub Copilot: Build Local Workspace Index`). Subsequent builds are faster than initial build.
- If your project has **>2500** indexable files, local index can't be built, only remote index can via `Ctrl + Shift + P` > `GitHub Copilot: Build Remote Workspace Index`.
- If your project has **>2500** indexable files and does not have a remote index, basic index is used.

## [Code review](https://docs.github.com/en/copilot/using-github-copilot/code-review/using-copilot-code-review?tool=vscode)

The power of OSS and FOSS is the community. Anyone who contribute their code to a public repository with active community can receive code audit from the author/maintainers.

However, for self-developing projects, without a code auditor there will be a lot of problem in the future. Using LLM as code auditor, a single developer can become a one-man army.

There are **TWO** types of review:

- **Review selection:** Highlight code and ask for a local review. **It's currently broken**
- **Review changes:** Review commits in a PR. Set at remote repository settings.

The review instructions can be taken from `CONTRIBUTING.md`.

## Web UI features

- Ask anything about a repository, a file, a GitHub Issue, ... I once do a code audit on a file and it found several bugs.
- Specify System Prompt. Solve blank page problem with this website: [https://prompts.chat/](https://prompts.chat/)

  ```
  You are a seasoned Python developer with over ten years of experience.
  When teaching, give practical examples after explaining each concept.
  Be concise and to-the-point.
  ```

## FAQ

**Q: Does GitHub Copilot Chat index EVERY file in workspace?**

A: According to [What sources are used for context?](https://code.visualstudio.com/docs/copilot/reference/workspace-context#_what-sources-are-used-for-context), here are the list of indexable and non-indexable files:

**Indexable**:

- Relavant text files inside workspace (seems ambiguous)
- Directory structure.
- GitHub Code Search index (if the workspace is a GitHub Repository and indexed by code search)
- Symbols and definitions in the workspace.
- Currently selected text + Visible text in the active editor.
- Conversation history

> [!CAUTION]
>
> The final input is hidden, I would like it to be transparent.

**Non-indexable:**

- `.tmp`, `.out`
- Anything in `files.exclude` VSCode setting JSON.
- Anything in `.gitignore` (except for files opened in active editor, or explicitly added)
- Binary files: images, PDFs, ...

---

**Q: Does GitHub Copilot use indexed repository for model training?**

A: [Copilot say "No"](https://docs.github.com/en/copilot/using-github-copilot/copilot-chat/indexing-repositories-for-copilot-chat#benefit-of-indexing-repositories), but don't trust them. Deploy local LLM in your workplace is the best solution.

## Yet another prompt engineering practice.

- Don't use coding guidelines to enforce style guidelines that can be covered by your linter or static analysis tool.
- Don't use wording that is ambiguous or could be interpreted in different ways.
- Don't fit multiple different ideas into a single coding guideline.

Consider the size and complexity of the repository to do and don't do the following:

- Refer to external resources.
- Instructions to answer in a particular style.
- Always respond with a certain level of detail.

## References

- [VSCode Docs's "Customize chat responses in VS Code"](https://code.visualstudio.com/docs/copilot/copilot-customization)
- [GitHub Docs's "About customizing GitHub Copilot Chat responses"](https://docs.github.com/en/copilot/customizing-copilot/about-customizing-github-copilot-chat-responses)
- [GitHub Docs's "Copilot Customization: Tips for defining custom instructions"](https://code.visualstudio.com/docs/copilot/copilot-customization#_tips-for-defining-custom-instructions)
- [GitHub Docs's "Dos and Don'ts for Coding guidelines"](https://docs.github.com/en/copilot/using-github-copilot/code-review/configuring-coding-guidelines#dos-and-donts-for-coding-guidelines)
