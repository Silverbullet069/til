# Best Security Practices in 2025

<!-- tl;dr starts -->

After being scared when I installed an NPM package directly from a GitHub repository, `npm` showed me a message indicating the package contained malware that could compromise my machine simply by installing it. Fortunately, a helpful Reddit user explained that it was a malicious package with the same name that had been pushed to the NPM registry and removed 3 years ago. Somehow `npm` just looked at the package name and warned me that the package installed from the official GitHub repository was compromised. This incident showed me that I need to update my security knowledge regarding the `npm` ecosystem specifically and all other package managers in general.

<!-- tl;dr ends -->

## Thread models

- One popular NPM package can contain hundreds of direct dependencies and thousands of transitive dependencies. One direct/transitive dependency get f\*\*ked and we're all f\*\*ked.

- `npm` hooks `pre-install` and `post-install` have full machine access and run silently. So does `pip` calling setuptools's post-install hook, `brew`, `yum`, ... Git hooks don't come with repo when you clone it, but that doesn't save you when you run any command, file or import from a git repo.

- Dependency auto updater is set up at most popular packages. NPM has no reidentification step for publishing package updating after the initial authentication via `npm login` or via an NPM configuration token stored in `~/.npmrc`. If a maintainer's machine is compromised, is hijacked or the maintainer himself goes rogue, they can push malicious updates to packages that millions of projects depend on, and those updates will be automatically distributed through the dependency chain.

- Disabling `pre-install`, `post-install` hooks can save you from being conpromised after installing it, but it won't save you after running it.

- Watching outbound network traffic and allow connected to a handful of known hosts is very hard. Your computer connects to thousands of hosts indicating where your HTML/CSS/JS scripts and static asset (images, videos, ...). Those files might not be served from source, they might be cached on various caching points on the vast CDN of many major cloud providers. No matter how restrictive your rules, hackers can bypass it by renaming your SSH upload endpoint to `imghostrr.com/puppy.png`

## What damaged can be done by a post-install script?

- Collect system information, your `.ssh`, `.gpg`, crypto wallet keys on a hacker's server. Control your machines, GitHub Repository, take your money, ...
- Download additional payloads.
- Install a silent daemon that puts a backdoor in your HTTPS connection.
- Install a crypto miners.
- Impersonate a package maintainer to update a package that includes the virus.
- Inject themselves into any ISO image you download on your computer.
- ...

## Real-world examples of package manager security incidents

1. **event-stream (2018)**: Popular NPM package with 2 million weekly downloads was compromised when maintainer transferred ownership to a malicious actor who injected cryptocurrency-stealing code targeting Copay wallet users.

1. **eslint-scope (2018)**: Compromised version 3.7.2 contained malicious code that stole NPM credentials from developers' machines and sent them to a remote server.

1. **ua-parser-js (2021)**: Popular browser detection library was hijacked and versions 0.7.29, 0.8.0, and 1.0.0 contained cryptocurrency miners and password stealers affecting millions of downloads.

1. **node-ipc (2022)**: Maintainer intentionally added destructive code that deleted files on Russian and Belarusian users' machines as a protest against the war in Ukraine, affecting dependent packages like Vue CLI.

1. **colors.js and faker.js (2022)**: Maintainer sabotaged their own widely-used packages by introducing infinite loops, breaking thousands of applications that depended on them.

1. **PyTorch (2022)**: Malicious dependency "torchtriton" was uploaded to PyPI that exfiltrated sensitive data from infected machines, affecting PyTorch nightly builds.

1. **ctx and phpass packages (2017)**: Typosquatting attack where malicious packages with similar names to popular ones harvested environment variables containing credentials and API keys.

1. **XZ Utils backdoor (2024)**: A sophisticated supply chain attack where a maintainer gradually introduced a backdoor into the XZ compression utility over several years. The backdoor specifically targeted SSH connections and could allow remote code execution on Linux systems. This incident highlighted how attackers can gain maintainer access to critical infrastructure packages and slowly introduce malicious code through seemingly legitimate commits.

1. **serve-static-corell, openssl-node and next-refresh-token packages (2024) [^9]**: these 3 packages contain obfuscated malicious payloads that would be executed upon **installation**, collecting details from the host machine and reaching out to a remote server to fetch more code to run.

[^9]: https://cycode.com/blog/malicious-code-hidden-in-npm-packages/

## Proposed practices

- Prevent `npm install/update` from installing packages with reported malware (likewise for `pip`, `brew`, `apt`, `yum`, ...)
- Always require re-authentication for package updates. It can be better if GitHub could do this.
- Have `npm` and `pypi` registry build the binaries and minified code themselves, instead of having users build the package and upload them.

## Mitigation (not elimination) practices

- Learn about [reproducible builds](https://reproducible-builds.org/).
- Secure development environment with [GitHub Codespaces](https://code.visualstudio.com/docs/remote/codespaces) and/or [Microsoft Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers).
- Secure deployment with containerized applications.
- Report the malware as quickly as possible on `npm`, `pip`, `brew`, ...
- Manual audit popular packages regularly and have a separte registry with only known, trusted software. This is the most secure but also the hardest practice since reading line-by-line takes a lot of time and effort.
- Setup security tools to automate auditing (some might slip past the detection algorithm, again, only a full transparent package + a team audit every single line of code can ensure maximum security).
- Stop distributing minified on build, only distribute source code, let the users build their own packages and let `gzip` compress the source files.
- Put passphrases on all your private keys.
- If you're package maintainer, stay logged out of your accounts on `npm`, `github`, ... at least in the CLI.
- Disable `npm` hooks `pre-install` and `post-install`.
- Use `deno` with hardened permissions instead of `node`.
- Use `firejail` to run `python` code. It's not too trouble, and it eases your overthinking mind.
- Use Rootless Docker, run as user, prevent privilege escalation with `--security-opt=no-new-privileges:true`.
- Do your work inside a GitHub Codespace, inside a VM, SSH to a single-use remote machine.
- `pip` and `npm` is more prone to attack than `apt` and `brew`. For `yum` I tried not to think about it (I'm a Fedora user).

Package lock files (package-lock.json)
Exact versions instead of ranges
npm audit regularly
Dependency scanning tools
