# GitHub Copilot best practices

<!-- tl;dr starts -->

This platform's potential is limitless. I was lucky when I get to use the tool myself to solve a variety of programming tasks.

<!-- tl;dr ends -->

## [Code completions](https://code.visualstudio.com/docs/copilot/ai-powered-suggestions)

## [Custom instructions](https://code.visualstudio.com/docs/copilot/copilot-customization)

**REMEMBER**: instructions should be used to skip the writing repetitive and tedious instructions to prompt. Don't try to enrich your response just because you have seen a very beautiful instructions from other developers.

Mainstream since [2024-10-29 release](https://code.visualstudio.com/docs/copilot/copilot-customization), until the time of writing, there are 4 types of instructions:

<!-- prettier-ignore -->
| Instruction types | Code-generation | Test-generation | Code review | Commit message |
|---|---|---|---|---|
| Use | Chat view, Quick Chat, Inline Chat. Doesn't apply to [Code Completions](#code-completions) | <ul><li>Chat view/Quick Chat: `@workspace /tests`</li><li>Select code, then open Inline Chat: `/tests`</li></ol> | `Ctrl + Shift + P` -> `GitHub Copilot: Review and Comment` | Source Control view -> Sparkle icon |
| Examples | <ul><li>`In TypeScript always use underscore for private field names.`</li><li>`Always add code comments.`</li><li>`Always use React functional components.`</li></ul> | <ul><li>`Always use vitest for testing React components.`</li><li>`Use Jest for testing JavaScript code.`</li></ul> | <ul><li>`Ensure all endpoints are protected by authentication and authorization`</li><li>`Validate all user inputs and sanitize data`</li><li>`Implement rate limiting and throttling`</li><li>`Implement logging and monitoring for security events`</li></ul>|[`Enforce conventional commits`](https://www.conventionalcommits.org/en/v1.0.0/)|
| Setup | `settings.json` and `.github/copilot-instructions.md` | `settings.json` | `settings.json` | `settings.json` |

Using `.github/copilot-instructions.md` is recommended, since it helps:

- Create reusable prompts for components, tests, migrations.
- Share specialized knowledge through prompts (e.g. optimization, security practice, compliance checks, ...)
-

For [**Code review**](https://docs.github.com/en/copilot/using-github-copilot/code-review/using-copilot-code-review?tool=vscode), there are 2 types:

- Review selection: (VSCode) Highlight code and ask for an initial review.
- Review changes:
  - [(VSCode)](https://docs.github.com/en/copilot/using-github-copilot/code-review/using-copilot-code-review?tool=vscode#working-with-suggested-changes-provided-by-copilot-1) Before creating a Pull Request, contributor can request a review to the changes firsthand. (AI can do part of human code auditors' jobs). [Setup at Repository settings using Web UI](https://docs.github.com/en/copilot/using-github-copilot/code-review/configuring-coding-guidelines).
  - [(Web UI)](https://docs.github.com/en/copilot/using-github-copilot/code-review/using-copilot-code-review?tool=webui#working-with-suggested-changes-provided-by-copilot) After creating a Pull Request, contributor can choose Copilot as the reviewer.

The power of OSS and FOSS is the community. Anyone can contribute their code to the repository, from the developer and maintainer team who knows the project like the back of their hand to the non-official developers happens to come across the project. But the latter aren't taught or trained to apprehand the coding standard, they solely rely on the documentation and communication methods to the official team through GitHub Issue/Discord/... worse, the existing code itself. Therefore, the code can be bad (or "smelly"), giving the reviewer a hard time to read.

> Whitespace between instructions is ignored, so the instruction can be written as a single paragraph, each on a new line, or separated by blank lines for legibility.

### [Tips for defining custom instructions](https://code.visualstudio.com/docs/copilot/copilot-customization#_tips-for-defining-custom-instructions)

- Keep your instructions short and self-contained. Each instruction should be a single, simple statement. If you need to provide multiple pieces of information, use multiple instructions.

- Don't refer to external resources in the instructions, such as specific coding standards.

- Make it easy to share custom instructions with your team or across projects by storing your instructions in an external file. You can also version control the file to track changes over time.

#### [Coding guidelines](https://docs.github.com/en/copilot/using-github-copilot/code-review/configuring-coding-guidelines#dos-and-donts-for-coding-guidelines)

- Do use simple, clear and concise language to describe your coding guideline.
- Do be as specific as possible about what Copilot should look for - that is, what you do or don't want to see in your code.
- Do take a look at the Coding guidelines examples below for some inspiration.
- Don't try to use coding guidelines to enforce style guidelines that can be covered by your linter or static analysis tool.
- Don't use wording that is ambiguous or could be interpreted in different ways.
- Don't try to fit multiple different ideas into a single coding guideline.

## Web Browser Chat Instructions

This feature came out on [2025-02-14 change log](https://github.blog/changelog/2025-02-14-personal-custom-instructions-bing-web-search-and-more-in-copilot-on-github-com/), applies when using GitHub Copilot Chat on [https://github.com/copilot/](https://github.com/copilot/).

User can specify custom preferences using natural languages. I personally do not recommend users to try to write their own preferences if they don't know how to express it with their own word. Their response can be worse than one without the preferences and they wouldn't even know about it.

Instead:

- On Web UI, preference template can be generated by clicking the light blub in the bottom-right corder of the instructions textarea.
- Use dedicated prompts directory as reference such as [https://prompts.chat/](https://prompts.chat/). Each prompt is designed and tested by experienced Prompt/AI Engineers.
- Take a look at some examples below for inspiration:
  - Language: `Always respond in Vietnamese.`
  - Response: `Be concise and to-the-point. Always cite your sources.`
  - Personal: `You are a seasoned React developer with ten years of experience.`
  - Code: `Always provide examples in Bash.`

My current instructions:

```
You are a seasoned Python developer with over ten years of experience.
When teaching, give practical examples after explaining each concept.
Be concise and to-the-point.
```
