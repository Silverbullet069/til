# Arbitrary Code Formatting Is Bad

<!-- tl;dr starts -->

Arbitrary code formatting is good if you're the author of the project, it saves you previous time to do something else more important. But when contributing to other open-source repository, it can create unnecessary change in PRs. Sometimes you won't even know it.

<!-- tl;dr ends -->

There are ways to control the behavior of code formatters in a per-project scope via configuration files:

- **VSCode/VSCodium**: `.vscode/settings.json`.
- **EditorConfig**: `.editorconfig`. Make sure to install [EditorConfig for Visual Studio Code extension](https://marketplace.visualstudio.com/items?itemName=EditorConfig.EditorConfig) first.
- **Prettier**: `.prettierrc`, `.prettierrc.json`, ... More supported extensions for configuration file can be found in [Prettier's Configuration File](https://prettier.io/docs/configuration).
