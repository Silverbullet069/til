# VSCode Chat Features and GitHub Copilot Chat Extension

<!-- tl;dr starts -->

Each VSCode monthly release introduces a lot of major breaking changes to AI features due to being under active development. The GitHub Copilot Chat extension is under active development as well. Everything is new, non-standardized and unstable. This is both a chance and a challenge to me. When LLMs and AI-powered platforms are new and not many people can effectively utilize them, I can get an upperhand before it becomes maturity and more people can fully grasp it.

<!-- tl;dr ends -->

## [Cheatsheet](https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features#_chat-variables)

- There are **THREE** chat UI: **Chat view**, **Quick Chat** and **Inline Chat**.
- Switch mode using `Ctrl + .`.
- `Show Chats` command can restore past sessions, even Edit/Agent sessions so you can keep working on them
- It is recommended to use **Open Chat in New Window** since you can run multiple agents at once. However, it is best to keep at most one agent use read-write tools, while the rest use read-only tools.

---

Since company might banned the use of 3rd-party LLMs. Use self-hosted SLM with Bring Your Own Key (BYOK) feature.

---

There are multiple types of [Contexts](https://code.visualstudio.com/docs/copilot/chat/copilot-chat-context) (for now, maybe more in the future)

- `@chat-participant` or `@chat-participant /command`.
- `#chat-variable`
- `Open Editors`
- `Files & Folders`
- `Screenshot Window`
- `Source Control` (add history item)
- `Instructions`
- `Problems`
- `Symbol`
- `Tools`

---

[Chat variables](https://code.visualstudio.com/docs/copilot/reference/copilot-vscode-features#_chat-variables) are list of tools/tool sets, either from built-in, custom grouped or Extensions.

Built-in:

- `#changes` (the list of source control changes)
- `#codebase`
- `#editFiles` (edit files directly)
- `#extensions`
- `#fetch` (fetch the main content of a web page whose URL is specified in any of the context)
- `#<file:foo.bar>` or `#<file:dir>` (attach a file/directory as context)
- `#findTestFiles` (given a code under test, output test file, and vice versa)
- `#githubRepo` (code search for a GitHub repo, e.g. `what is variable reference in VSCode #githubRepo microsoft/vscode`)
- `#new` (scaffold new VSCode workspace)
- `#openSimpleBrowser` (open built-in browser, preview a locally-deployed web app)
- `#problems` (add workspace problems)
- `#runCommands` (running terminal commands)
- `#search` (search and read files inside workspace)
- `#searchResults` (add results from Search view a.k.a Find and Replace input field)
- `#selection`
- `#<symbol>` (add symbol name, require language servers)
- `#terminalSelection`
- `#terminalLastCommand`
- `#testFailure` (add test failure info from VSCode's test feature)
- `#usages` ("Find All References" + "Find Implementations" + "Go to Definition").
- `#VSCodeAPI` (**NOTE:** ask questions releated to VSCode **extension development**)
- `#<tool-set>` (a collection of related tools grouped together and toggleable in Agent mode).

Python Extension:

- `#configurePythonEnvironment` (ensure Python Environment is set up correctly for the workspace, create virtual env if needed and activate it)
- `#getPythonEnvironmentInfo`
- `#getPythonExecutableCommand`
- `#installPythonPackage`

MermaidChart Extension:

- `#get_syntax_docs`
- `#mermaid-diagram-preview`
- `#mermaid-diagram-validator`

---

**Chat participants** are like "expert" of a field, and this "expert" can perform a list of pre-defined actions.

Run `/help` command to list all of the available Chat participants and their associating Chat commands.

> Without knowing the design decisions, the Chat participants can be hard to have its purpose understood.

```md
`@workspace`
`@workspace /explain`
`@workspace /tests`
`@workspace /fix`
`@workspace /new` (scaffold a new file/project in a workspace)
`@workspace /setupTests` (experimental)

`@github`

`@vscode`
`@vscode /search` (workspace search)

`@terminal`
`@terminal /explain`

`@mermaid-chart`
`@mermaid-chart /generate_cloud_architecture_diagram`

`/mcp.servername.promptname` (MCP prompts)
```

---

**THREE** main ways to [customize AI responses in VSCode](https://code.visualstudio.com/docs/copilot/copilot-customization): **instructions**, **prompts** and **custom chat modes**

---

**THREE** built-in [chat modes](https://code.visualstudio.com/docs/copilot/chat/chat-modes): **Ask**, **Edit** and **Agent**. New VSCode features allow users to define their own [**custom chat modes**](https://code.visualstudio.com/docs/copilot/chat/chat-modes#_custom-chat-modes).

---

**TWO** ways of using Copilot inside editor:

- GitHub Copilot's Code Completions: Code comments, Next Edit Suggesion (NES).
- GitHub Copilot Chat's Inline Chat: `Ctrl + I`.

---

## VSCode's Chat features

### Chat View in New Window UI

- Always on Top
- Toggle Compact mode
- New Chat

### Select and attach UI elements to chat

Set to true the following settings:

- `chat.sendElementsToChat.enabled`
- `chat.sendElementsToChat.attachCSS`
- `chat.sendElementsToChat.attachImages`

### Create and launch tasks in Agent mode

Set to true the following settings:

- `github.copilot.chat.newWorkspaceCreation.enabled`

### Chat tool sets

Run `Configure Tool Sets > Create new tool sets file` command to create a tool set.

Example: Manage GitHub notifications using GitHub MCP server

```jsonc
{
  "gh-news": {
    "tools": [
      "list_notifications",
      "dismiss_notification",
      "get_notification_details"
    ],
    "description": "Manage GitHub notification",
    "icon": "github-project"
  }
}
```

### [MCP](https://code.visualstudio.com/docs/copilot/chat/mcp-servers)

- Configuration: `"mcp"` section in user, remote `settings.json`, or `.code-workspace` settings, in `.vscode/mcp.json`.
  - Reference an env var using `${env:API_KEY}`
  - Prompt a value when server started `${input:ENDPOINT}`
- Can be installed via `MCP: Add Server`. However, MCP server can run arbitrary code on host system, best to set up Docker container.
- List MCP servers + status with `MCP: List Servers` command.
- Pick the tools available for use in chat using `Select Tools` button.
- Support Streamable HTTP and Stdin servers.
- Prompt:
  - MCP can implement the feature of generating prompt from prompt.
  - Accessible as slash commands `/mcp.servername.promptname`.
- Resources:
  - MCP tool calls result in resources.
  - Those resources can be saved in Chat.
  - Resources can be attached as Context.
  - List resources inside multiple MCP servers with `MCP: Browse Resources` command or one MCP server with `MCP: List Servers` command.
- Sampling/Auth
-

## VSCode Extension

### [Code review](https://docs.github.com/en/copilot/using-github-copilot/code-review/using-copilot-code-review?tool=vscode)

> [!CAUTION]
>
> Local code review features is bad. But PR code reviews is decent.

The power of OSS and FOSS is the community. Anyone who contribute their code to a public repository with active community can receive code audit from the author/maintainers.

However, for self-developing projects, by setting up LLM as code auditor, a single developer can become a whole tech division.

There are **TWO** types of review:

- **Review selection** or local review. Review code in active editor.
- **Review changes** or remote review. Review commits in a PR.

Select the part you want to review inside active editor and run `GitHub Copilot: Review and Comment` command to start

Tips: If you're contributing to OSS/FOSS projects, the review instructions can be taken from `CONTRIBUTING.md`.

### [Ask mode](https://code.visualstudio.com/docs/copilot/chat/chat-ask-mode)

Use cases:

- Asking questions about codebase, coding, general tech concepts.
- Understand how a random piece of code works.
- Brainstorm software design ideas.
- Explore new tech stack.

### [Edit mode](https://code.visualstudio.com/docs/copilot/chat/copilot-edits)

Use cases:

- Make code simple edits across multiple files in workspace.
- Simple coding tasks when: you know what needs to change and which files to edit.
- Lightweight operation with zero-to-few tool (set) are used.

### [Agent mode](https://code.visualstudio.com/docs/copilot/chat/chat-agent-mode)

Use cases:

- Make complex code edits across multiple files in workspace.
- Complex coding tasks when you have a less well-defined task. Terminal commands running
- Heavyweight operations with a lot of tool (set) are used: `fetch`, terminal commands running, etc.

> [!CAUTION]
>
> Auto approval all tools is dangerous. Set `chat.tools.autoApprove` to `false`

### [Custom modes (preview)](https://code.visualstudio.com/docs/copilot/chat/chat-modes#_custom-chat-modes)

Define how chat operates, which tools it can use and how it interacts with the codebase. Chat prompt is run within the boundaries of the Chat mode, without having to configure tools or instructions for every request.

To create a `*.chatmode.md` Markdown file:

- Run `Chat: New Mode File` command
- Choose either `.github/chatmodes` (workspace) or `~/.config/VSCode/User/prompts` (User profile).
- Chat modes in workspace are looked for first.
- Enter name.
- Write `description:` and `tools:` in frontmatter, write _instructions_ in the body.
- In Chat view, hit `Ctrl + .` to change chat mode.
- Manage existing chat modes with `Chat: Configure Chat Modes` command.

Use cases:

- `Planning` mode: consists of read-only tools `codebase`, `fetch`, `search`, etc. to generate implementation plans.
- `Research` mode: consists of read-only tools: `fetch`, tec. to explore new tech stack or gather information.
- `Front-end Developer` mode: AI has read-write access to the code related to front-end development.

Structure:

```yml
# plan.chatmode.md
---
description: Generate an implementation plan for new features or refactoring existing code.
tools: ["codebase", "fetch", "search"] # built-in tool, tool sets, MCP tools, Extension tools
---
```

```md
# Planning mode instructions

You are in planning mode. Your task is to generate an implementation plan for a new feature or for refactoring existing code.
Don't make any code edits, just generate a plan.

The plan consists of a Markdown document that describes the implementation plan, including the following sections:

- Overview: A brief description of the feature or refactoring task.
- Requirements: A list of requirements for the feature or refactoring task.
- Implementation Steps: A detailed list of steps to implement the feature or refactoring task.
- Testing: A list of tests that need to be implemented to verify the feature or refactoring task.
```

### [Instructions](https://code.visualstudio.com/docs/copilot/copilot-customization#_custom-instructions)

Define common guidel\ines/rules/... and should be added automatically by design

There are also **THREE** instructions types, remember to make them not conflicting themselves

1. **One-size-fit-all file:**

- **Description:** Describe Code Generation instructions in Markdown in a single file.
- **Format and scope:** Markdown file, workspace-level.
- `settings.json`:
  ```jsonc
  "chat.promptFiles": true,
  "github.copilot.chat.codeGeneration.useInstructionFiles": true,
  ```
- **Creation:** Create `.github/copilot-instructions.md` file.
- **Attach behavior:**
  - Manual: none
  - Automatic: in every Chat request.
- **Supported platform:** all code editors and IDEs supporting GitHub Copilot Chat.
- **Use cases:** general coding practices, preferred technologies, project requirements that apply to ALL code generation tasks.
- **Examples:**

`general-coding-guidelines.instructions.md`:

```yml
---
applyTo: "**"
---
```

```md
# Project general coding standards

## Naming Conventions

- Use PascalCase for component names, interfaces, and type aliases
- Use camelCase for variables, functions, and methods
- Prefix private class members with underscore (\_)
- Use ALL_CAPS for constants

## Error Handling

- Use try/catch blocks for async operations
- Implement proper error boundaries in React components
- Always log errors with contextual information
```

---

`typescript-react.instructions.md`:

```yml
---
applyTo: "**/*.ts,**/*.tsx"
---
```

```md
# Project coding standards for TypeScript and React

Apply the [general coding guidelines](./general-coding.instructions.md) to all code.

## TypeScript Guidelines

- Use TypeScript for all new code
- Follow functional programming principles where possible
- Use interfaces for data structures and type definitions
- Prefer immutable data (const, readonly)
- Use optional chaining (?.) and nullish coalescing (??) operators

## React Guidelines

- Use functional components with hooks
- Follow the React hooks rules (no conditional hooks)
- Use React.FC type for components with children
- Keep components small and focused
- Use CSS modules for component styling
```

2. `*.instructions.md` file

- **Description:** Describe **Code Generation** instructions in Markdown in one or more files.
- **Scope and format:**
  - Markdown files, workspace-level.
  - Markdown files, User profile level.
- **Settings:**
  ```jsonc
  "chat.promptFiles": true,
  "chat.instructionsFilesLocations": {
    "src/frontend/instructions": true,
    "src/backend/instructions": true,
  }
  ```
- **Creation:**
  - Hit `Ctrl + Shift + P` -> `Chat: New Instructions File`.
  - Choose `.github/instructions` if creating workspace-level file.
  - Choose `.config/VSCodium/User/prompts` if creating User profile level file.
- **Attach behavior:**
  - Manual: `Ctrl + /` -> `Instructions...`
  - Automatic: depends on `applyTo:` frontmatter.
- **Supported platform:** VSCode and their forks.
- **Use cases:** task-specific rules requiring fine-grained control over when to include in Chat request.
- **Structure and examples:**

  ```yml
  ---
  description: "A brief description of the instructions file. Displayed when users hovered the instructions file in the Chat view."
  applyTo: "**"                 # instructions attached to all Chat request
  applyTo: "**/*.sh,**/*.bash"  # instructions attached to Chat requests whose context is file with specific extensions
  ---
  Insert body here...
  ```

3. **VSCode Settings**

- **Description:** Describe 5(for now) different types of instructions.
- **Scope and format:**
  - Text inside workspace-level `.vscode/settings.json` or a workspace-level Markdown file.
  - Text inside User profile level `~/.config/VSCode/User/settings.json` or a workspace-level Markdown file.
- **Settings:**
  ```jsonc
  "github.copilot.chat.codeGeneration.instructions": [
    {
      "file": ".copilot-codeGeneration-instructions.md"
    },
    {
      "text": "Always add a comment: 'Generated by Copilot'.",
      "language": "markdown" // Language Identifiers: https://code.visualstudio.com/docs/languages/identifiers#_known-language-identifiers
    }
  ],
  "github.copilot.chat.testGeneration.instructions": [],
  "github.copilot.chat.reviewSelection.instructions": [],
  "github.copilot.chat.commitMessageGeneration.instructions": [],
  "github.copilot.chat.pullRequestDescriptionGeneration.instructions": []
  ```
- **Attach behavior:**
  - Manual: none
  - Automatic: all or specific files via `language:` property
- **Use cases:** general, one-size-fit-all rules for code generation, test generation, code review, commit messages generation and PR titles and descriptions generation.
- **Examples:**

  ```md
  <!-- code generation -->

  Always add a comment
  In TypeScript always use underscore for private field names
  Always use React functional components

  <!-- code review -->

  Ensure all endpoints are protected by authentication and authorization
  Validate all user inputs and sanitize data

  <!-- test generation -->

  Always use vitest for testing React components
  Implement rate limiting and throttling
  Implement logging and monitoring for security events

  <!-- commit message generation -->

  {{insert [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) here}}

  <!-- PR Description generation -->

  Include every commit message in the pull request description
  ```

### [Prompts](https://code.visualstudio.com/docs/copilot/copilot-customization#_prompt-files-experimental)

- **Description:** Ad-hoc reusable prompts. Prompt files reflect what user types in Chat input panel, utilizes all 4 prompt elements. It's different from Instructions who focuses on **rules**.
- **Scope and format:**
  - **Markdown files** with `.prompt.md` file suffix, **workspace-level** or **User profile level**.
- Settings:
  ```jsonc
  "chat.promptFiles": true,
  "chat.promptFilesLocations": {
    ".github/prompts": false, // rel path are resolved from the root folders of the workspace
    "setup/**/prompts": true  // glob patterns supported
  }
  ```
- Creation:
  - Create `.github/prompts` directory (location chosen by default, specify addition locations with `chat.promptFilesLocations` setting).
  - Hit `Ctrl + Shift + P` -> `Chat: New Prompt File`
  - Choose `.github/prompts` to create **workspace-level** file.
  - Choose `.config/VSCodium/User/prompts` to create **User profile level** file.
- Usage:
  - Method #1: `Ctrl + Shift + P` -> `Chat: Run Prompt` -> Select a prompt file from Quick Pick UI.
  - Method #2: In Chat view, type Chat command syntax: `/` followed by the prompt file name in the Chat input field. **TIPS:** it can provide value for _input variables_.
  - Method #3: Open the prompt file in the current active editor, press the Play button in the editor title area. **TIPS:** this method is less commonly known, but it's useful for quickly testing and iterating on your prompt files.
- Tips:

  - Refer to additional workspace files ("dependencies") using Markdown links (e.g. `[index](./index.ts)`) or Chat variable syntax (e.g. `#index.ts`)
  - Refer to [VSCode's variables](https://code.visualstudio.com/docs/reference/variables-reference) by using `${variableName}` syntax. Some supported variables are:
    - Workspace variables: `${workspaceFolder}`, `${workspaceFolderBasename}`.
    - Selection variables: `${selection}`, `${selectedText}`.
    - File context variables: `${file}` (the content of currently opened file), `${fileBasename}` (currently opened file's name), `${fileDirname}` (the parent directory of currently opened file)
    - Input variables: `${input:variableName}`, `${input:variableName:placeholder}` (pass values to the Prompt file from the Chat input field, e.g. `/create-react-form: formName=MyForm` )

- Structure and Examples:

  Generate a React form component

  ```yml
  ---
  mode: "agent" # "ask", "edit"
  tools: ["githubRepo", "codebase"] # array of tool (set) which would be used in Agent mode.
  # NOTE: select Configure Tools to toggle the tools of the list of available tools in your workspace.
  description: "Generate a new React form component"
  ---
  ```

  ```md
  Your goal is to generate a new React form component based on the templates in #githubRepo contoso/react-templates.

  Ask for the form name and fields if not provided.

  Requirements for the form:

  - Use form design system components: [design-system/Form.md](../docs/design-system/Form.md)
  - Use `react-hook-form` for form state management:
  - Always define TypeScript types for your form data
  - Prefer _uncontrolled_ components using register
  - Use `defaultValues` to prevent unnecessary rerenders
  - Use `yup` for validation:
  - Create reusable validation schemas in separate files
  - Use TypeScript types to ensure type safety
  - Customize UX-friendly validation rules
  ```

  ***

  Perform a security review of a REST API.

  ```yml
  ---
  mode: "edit"
  description: "Perform a REST API security review"
  ---
  ```

  ```md
  Perform a REST API security review:

  - Ensure all endpoints are protected by authentication and authorization
  - Validate all user inputs and sanitize data
  - Implement rate limiting and throttling
  - Implement logging and monitoring for security events
  ```

### [Indexing mechanism](https://code.visualstudio.com/docs/copilot/reference/workspace-context)

There are three types of indexes, ordered from least to most robust:

- **Basic index**
- **Local index**
- **Remote index**.

Logic:

- If your project has **<750** indexable files, local index is built **automatically**.
- If your project has **750-2500** indexable files, local index must be built **manually** (via `Ctrl + Shift + P` -> `GitHub Copilot: Build Local Workspace Index`). Subsequent builds are faster than initial build.
- If your project has **>2500** indexable files, local index can't be built, only remote index can via `Ctrl + Shift + P` > `GitHub Copilot: Build Remote Workspace Index`.
- If your project has **>2500** indexable files and does not have a remote index, basic index is used.

### Web UI features

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
