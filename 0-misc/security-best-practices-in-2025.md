# Best Security Practices in 2025

<!-- tl;dr starts -->

After being scared when I installed an NPM package directly from a GitHub repository, `npm` showed me a message indicating the package contained malware that could compromise my machine simply by installing it. Fortunately, a helpful Reddit user explained that it was a malicious package with the same name that had been pushed to the NPM registry and removed 3 years ago. Somehow `npm` just looked at the package name and warned me that the package installed from the official GitHub repository was compromised. This incident showed me that I need to update my security knowledge regarding the `npm` ecosystem specifically and all other package managers in general.

<!-- tl;dr ends -->

## The current conditions

Let's dive in the THREE categories of programs: Runtime, Package Manager and Runtime Version Manager

### Runtime (Node, Deno, Bun, Python, Ruby, ...)

Node, Python, etc. have no sandbox model.

Deno, Dart requires users to list both direct dependencies and transitive dependencies, which is a good auditing practice.

Deno's runtime, `wasmtime` - runtime for WebAssembly has a sandbox: it's designed with blacklist by default and whitelist by manual.

### Package Manager (or Build System) (npm/pnpm/yarn/...)

`git:`

- Git hooks by default don't get pushed into remote repository, but a malicious actor can set the `core.hookspath` setting's value to a directory that can be pushed and write the setting into a local Git config file so it can be automatically applied when users cloned the repo.
- In general, run any `git ...` command inside a repo can trigger anything.

`npm:`

- `npm install` executes the `pre-install` and `post-install` hooks from **hundreds** of direct dependencies and **thousands** of transitive dependencies. It takes only **ONE** dependency to f\*\*ked up our system.
- `npm install` has **full** system access yet ran silently.
- `npm` has dependency auto updater feature. It's not a good practice to turn this on, every dependencies should be manually audited.
- `npm` has no re-identification process for publishing package updates after initial auth via `npm login`, or via config token stored inside `~/.npmrc`. A maintainer's compromised machine can push malicious updates easily
- Disabling `pre-install` and `post-install` hooks can save you when running `npm install` but can't save you when you're actually running it. Not to mention it could lead to breakage of the "good" hooks.

`pip:`

- `setuptools` has a `post-install` hook.
- `pip` also have full system access.

### Runtime Version Manager (nvm, pyenv, rvm, ...)

None of them have sandbox.

## What damaged can be done ?

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

1. **node-ipc (2022)**: Maintainer intentionally added destructive code that deleted files on Russian and Belarusian users' machines as a protest against the war in Ukraine, affecting dependent packages like Vue CLI. **This is one of the reason shows that you can't even trust the package maintainers.**

1. **colors.js and faker.js (2022)**: Maintainer sabotaged their own widely-used packages by introducing infinite loops, breaking thousands of applications that depended on them.

1. **PyTorch (2022)**: Malicious dependency "torchtriton" was uploaded to PyPI that exfiltrated sensitive data from infected machines, affecting PyTorch nightly builds.

1. **ctx and phpass packages (2017)**: Typosquatting attack where malicious packages with similar names to popular ones harvested environment variables containing credentials and API keys.

1. **XZ Utils backdoor (2024)**: A sophisticated supply chain attack where a maintainer gradually introduced a backdoor into the XZ compression utility over several years. The backdoor specifically targeted SSH connections and could allow remote code execution on Linux systems. This incident highlighted how attackers can gain maintainer access to critical infrastructure packages and slowly introduce malicious code through seemingly legitimate commits.

1. **serve-static-corell, openssl-node and next-refresh-token packages (2024) [^9]**: these 3 packages contain obfuscated malicious payloads that would be executed upon **installation**, collecting details from the host machine and reaching out to a remote server to fetch more code to run.

[^9]: https://cycode.com/blog/malicious-code-hidden-in-npm-packages/


## Mitigation strategy

I will list the number of strategies from the easiest, fastest, restrictive-enough to the hardest, slowest and most restrictive:

- `pip` and `npm` is more prone to attack than `apt` and `brew`. For `yum` I tried not to think about it (I'm a Fedora user).

- Use `firejail node|yarn|python|... ` to wrap the Runtime and Package Managers. There might be times when you forget to prefix `firejail ...` so it's best to create symlinks:

```bash
# Define an array of executables to sandbox
# NOTE: update this array
executables=(node npx npm)

for exe in "${executables[@]}"; do
  # Create symlinks for each executable
  sudo ln -s /usr/bin/firejail "/usr/local/bin/${exe}"

  # Append each {exe}cutable to firejail's firecfg.config
  echo "$exe" | sudo tee -a /etc/firejail/firecfg.config
done
```

- Use Rootless Docker, run as user, disable network, enable read-only filesystem (or read-only mounted volumes) and prevent privilege escalation.

```bash
docker run \
  --name="image_name" \
  --init \
  --rm \
  --user="$(id -u):$(id -g)" \
  --read-only  \
  --network="none" \
  --security-opt="no-new-privileges:true" \
  --volume="${PWD}:/app:ro" \
  --workdir="/app" \
  # an alpine-based iamge
  silverbullet069/image_name:latest \
  "$@"
```

- Put passphrases on all your private keys.

- For JavaScript backend developers: disable `npm` hooks `pre-install` and `post-install`, use `deno` with hardened permissions .

- Set up package monitoring tools like Socket, Snyk, etc. to prevent allowing package managers from installing packages with reported malware.

- Develop your applications while following [reproducible builds](https://reproducible-builds.org/) practices.

- Secure your development environment using containerization: [GitHub Codespaces](https://code.visualstudio.com/docs/remote/codespaces) and [Microsoft Dev Containers](https://code.visualstudio.com/docs/devcontainers/containers) or a VM.

- Secure the deployment environment using containerization in your CI/CD pipeline.

- If you're a package maintainer, create a re-auth process for yourself. Don't wait for the package manager to do it for you. Also stay logged out of your accounts on `npm`, `github`, etc. If you can't, at least in the CLI.

- If you're skillful enough to identify an undisclosed malware, report it as quickly as possible.

- Manual audit popular packages regularly and have a separate registry with only known, trusted software.
  > The most secure practice, but also the hardest. Only Google has reported to adhere this practice by auditing line-by-line of every tech stack it uses.

- Setup security tools to automate auditing using both:
  - Static analysis tool (some might slip past the detection algorithm, again, only a full transparent package + a team audit every single line of code can ensure maximum security).
  - Dynamic analysis tool (using LLM, more reliable but slow and expensive). **NOTE: yet, nobody has ever done it?**

- Watching outbound network traffic and allow connected to a handful of known hosts.
  > Very hard. Your computer connects to thousands of hosts indicating where your HTML/CSS/JS scripts and static asset (images, videos, ...). Those files might not be served from source, they might be cached on various caching points on the vast CDN of many major cloud providers. No matter how restrictive your rules, hackers can bypass it by renaming your SSH upload endpoint.

## Proposed practices

- Have `npm` and `pypi` registry build the binaries and minified code themselves, instead of having users build the package and upload them.
- Stop distributing minified on build, only distribute source code, let the users build their own packages and let `gzip` compress the source files.

<!-- TODO: finish learning the following -->
Package lock files (package-lock.json)
Exact versions instead of ranges
npm audit regularly
Dependency scanning tools

## References

- [Comparing Sandbox Tools](https://hkubota.wordpress.com/2020/12/31/comparing-sandboxing-tools/)
