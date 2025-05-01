# VSCode Extension Project Structure

<!-- tl;dr starts -->

When I make [my first VSCode Extension for my graduated thesis](https://github.com/Silverbullet069/delopa), I'm a lousy engineer when it comes to design. But now it's the first thing I do.

<!-- tl;dr ends -->

```
├── .vscode/                  # VS Code settings
│   ├── launch.json           # Debug configuration
│   └── tasks.json            # Build tasks
│   └── settings.json         # VS Code workspace settings
├── .github/
│   ├── copilot-instructions.md # System prompts for TypeScript in general and VSCode Extension in specific
├── ai_models/                # Local Python AI models
│   ├── ...
├── src/                      # Source code
│   ├── commands/             # Focus on user invoker operations, thin wrappers around services/
│   │   ├── index.ts          # Command registration
│   │   └── myCommand.ts      # Individual command implementation
│   ├── providers/            # Editor enhancement
│   │   ├── MyViewProvider.ts # Webview/Tree view provider
│   │   └── DiagnosticsProvider.ts
│   ├── services/             # Core business logic
│   │   └── myService.ts      # Service implementation
│   ├── utils/                # Helper (pure) functions
│   │   └── fileUtils.ts      # Utility functions
│   ├── constants.ts          # Constants and configuration
│   └── extension.ts          # Extension entry point
├── docs/                     # Documentation
│   ├── myDocs.md             # Writing Markdown file to document your feature here
├── test/                     # Tests
│   ├── suite/
│   │   ├── extension.test.ts # Test file
│   │   └── index.ts          # Test entry
│   └── runTest.ts            # Test runner
├── webview/                  # Webview front-end (optional)
│   ├── main.js               # Webview JavaScript
│   └── style.css             # Webview styles
├── media/ or resources/      # Static assets
│   ├── icon.png              # Extension icon
├── .eslintrc.json            # ESLint config
├── .gitignore                # Git ignore file
├── CHANGELOG.md              # Change log
├── LICENSE                   # License file
├── package.json              # Extension manifest
├── README.md                 # Overview/simple documentation
├── tsconfig.json             # TypeScript config
└── webpack.config.js         # Webpack config (optional)
```

<!-- TODO: run the examples inside this link and document them here: https://github.com/copilot/share/8a6210a4-4900-8c41-9800-040d80106823-->
