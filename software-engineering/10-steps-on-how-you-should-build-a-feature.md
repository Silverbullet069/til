# 10 Steps On How You Should Build A Feature?

<!-- tl;dr starts -->

When I first saw Simon Willison's way of building features that can boost productivity on hundreds of personal projects at the same time, I knew I have found my ultimate methodology.

<!-- tl;dr ends -->

### Step 1: Create a verson control repository from a template and set up the development environment

Start by creating a GitHub repository. To save time and effort, use **an existing template** or **create your own template** if the tech stack of the existing template does not align with yours.

This template should have everything set up for you:

- A README.md acts as simple documentation.
- A repository file `LICENSE.md`.
- A [contribution guidelines](https://en.wikipedia.org/wiki/Contributing_guidelines) `CONTRIBUTING.md`
- A security instructions file `SECURITY.md`.
- A Code of conduct.
- A `tests/` directory set up a dummy test case.
- CI/CD (GitHub Actions `.github/workflow/*.yml` file)
- A Git hooks framework such as [typicode/husky](https://typicode.github.io/husky/). It can lint your commit messages, code and run integration tests automatically.
- Security (GitHub Dependabot alerts `.github/depandabot.yml`, setup Branch protection rules to protect import branches, Secret scanning, Code scanning, Private vulnerability reporting, ...)

_Examples:_

- [simonw/click-app](https://github.com/simonw/click-app)
- [simonw/python-lib](https://github.com/simonw/python-lib)
- [CodeStitchOfficial/Intermediate-Website-Kit-SASS](https://github.com/CodeStitchOfficial/Intermediate-Website-Kit-SASS)
- [rochacbruno/python-project-template](https://github.com/rochacbruno/python-project-template/)

These GitHub Repository templates whose dynamic content should be able to be populated by [GitHub Actions](https://simonwillison.net/2021/Aug/28/dynamic-github-repository-templates/).

Using VSCode's Code Snippet feature to add reusable code snippets. I recommended you extract from the cheatsheet of the tech of your stack.

### Step 2: Create an issue and research the problem

Everything starts with an issue thread on your chosen version control system. The issue contains multiple comments recording your research and real progress while you're working on the feature.

_**EIGHT** components in an issue:_

1. **Background:** the purpose/goal of the feature, the reason for the change, use case story, UI/UX requirement, ...
1. **State of play before-hand:** existing code snippets from similar features from similar tools and links to existing docs.
1. **Reference:** tech documentation, blog, forum Q&A, ... It's like capturing those loose information sources and turning them into knowledge.
1. **Design decision**: note down all of your design decisions
   - Top-down or bottom-up.
   - Directory structure.
   - Workflow diagram.
   - CLI `--help`.
   - Database schema.
   - ...
1. **Attempt:** code snippets illustrating potential designs and false-starts. Again, do not start coding right away to minimize # of iterations.
1. **Screenshot:** your product's UI before and after. Animated screenshots are prefered ([LICEcap](https://www.cockos.com/licecap/) or [QuickTime](https://support.apple.com/en-vn/106375))..
1. **Prototypes:** a Python REPL session, a block of HTML and CSS, a quick snap from [CodeSnap](https://codesnap.dev/) ... anything that showcase the final decision.
1. **After closed**: a link to the updated documentation and a live demo of the new feature (optinally).

_**SIX** pros:_

- **Issue-driven:** The issue is the thing that comes first before everything else, thus solving the **blank-page** problem.
- **Issues over Commit messages:** Detailed issue threads is more valuable than long commit messages.
  > Simon stated that he received a net increase in his overall productivity.
- **Asynchronous:** By recording your research and real progress, you can leave it there and pick up the work later. Next time you won't waste time researching again.
- **Scalability:** A simple feature may result in a single issue with one comment (usually opened and closed immediately with a small commit containing only a few lines of code), while a complex feature can span across multiple issues and PRs with hundreds of comments and commits.
- **Bidirectional references**: Any commit can relate to an issue, likewise you can navigate from the issue to any related commits. The same applies to the relationship between release notes and issues.
- **Temporary and informal documentation:** Issues are written in conversational language and serve as commitment-free, informal documentation, making them easy to write. Most importantly, no one will be upset or confused if issue comments do not match the final implementation.

_**THREE** practices:_

- **DO NOT FORGET:** Inexperienced practitioners often start coding right away without conducting any research firsthand.
- **Archive issue threads:** maintained a SQLite database on cloud for all of the issues and their comments.
- **Switch to PRs to receive code audit from LLMs:** When you know you're going to make a lot of WIP commits, don't hesitate to create a PR and relocate your research there. GitHub Copilot can audit your code in a PR. This is a hugh benefit for solo developers like me who sometimes forgot the power of PR.

> IMO, issues resembles the history of features. Learning history always give us a better insight, it applies to a range of subjects beside computer science, such as physics, chemistry, biology and literature. No.4 component - **Design decision** is the most crucial yet they're often being omitted in official documentation.

_Examples:_ Issue thread's title

```
Initial research (tag: good first issue)
TOOL_NAME COMMAND_NAME command (tag: enhancement)
COMMAND_NAME tests failing (tag: bug)
Suggestion: blah blah blah
Design the blah blah blah
Research the blah blah blah
```

### Step 3: Determine the branching strategy

There are a lot of branching strategy that's appropriate to different projects depending on its scope, team size, ... Here are some of the most popular strategies:

1. **Gitflow:** using two primary branches `main/master` and `develop` with multiple supporting branches with prefix `features/*`, `hotfix/*`, `release/*`, ...

```sh
# branch from develop
$ git checkout develop
$ git pull origin develop # update changes from other team members
$ git checkout -b feature/mock

# work + make WIP commits
$ git add .
$ git commit -S -m "feat/docs/test: WIP commit"

# Here, you have two options:
# ======================================================================= #
# Option 1: prevent rewriting history in the first place by reflecting develop
# branch every time you want to push your branch.
# IMO, it's tedious and impractical
$ git fetch origin develop
$ git rebase origin/develop
$ git push origin feature/mock # in the future, you only need to run `git push/git pull` and it will automatically know which branch to work on
# ======================================================================= #
# Option 2: fxxk it, just push
$ git push origin feature/mock
# ======================================================================= #

# Then, Open PR: feature/mock -> develop
$ gh repo set-default
$ gh pr create --base develop --editor --fill
# ======================================================================= #
# If you choose option 1, stop reading here.
# ======================================================================= #

# During code review, you push some more WIP commits
$ git add .
$ git commit -S -m "wip: reflect code auditors' feedback"
$ git push origin feature/mock

# finally, use the "squash and merge" strategy in GitHub PR's Web UI.
# One PR = One atomic commit.

# ======================================================================= #
# If you don't have merge conflicts with develop branch, stop reading here
# ======================================================================= #

# When everything is okay, make sure your feature branch and the develop branch's
# current state does not have merge conflicts
$ git checkout feature/mock
$ git fetch origin feature/mock

# CAUTION: DO NOT simply run `git fetch + git merge` nor `git pull` here.
# Without specifying a particular remote and branch, by def `git fetch` will
# fetch ALL branches from the default remote (usually `origin`) and updates ALL
# corresponding remote-tracking branches (e.g. `remote/origin/main`, `remote/origin/develop`, ...)
# more specifically, the local copies of remote branches on your machine.
# $ git branch -r  # check the copies
# by doing so,
# Cre: https://stackoverflow.com/a/59413159/9122512

$ git rebase [-i] origin/develop

# meanwhile, develop has new commits.
# develop:        A---B---C
#                  \
# feature/mock:     D---E

# git rebase performs these steps
# 1. identify the common ancestor of feature branch and main branch, which is commit A
# 2. save the feature branch's commits (D, E) as temporary patches.
# 3. reset feature branch to match main (A, B, C)
# 4. replay feature branch commit on top of the new feature branch, now called D' and E'

# Result
# develop:        A---B---C
#                  \
# feature/mock:     D'---E'

# the rebased commits receive new SHA hashes.
# the commit dates of rebased commits are updated to the current time.

# during rebase, there might be merge conflicts ...
$ git rebase --continue
$ git push [--set-upstream] --force-with-lease --force-if-includes origin feature/mock # failed if the tip of origin/feature/mock (on remote, not the local copy) can't be found on the local feature/mock
$ git fetch origin feature/mock
$ git rebase [-i] origin/feature/mock
$ git push [--set-upstream] --force-with-lease --force-if-includes origin feature/mock # now it should be succeed

# After that, use "Squash and Merge" option to add a big commit on top of `develop` branch
# The squashed commit becomes the Perfect Commit with atomic changes

# When ready for release, merge develop to main
$ git checkout main
$ git pull origin main
$ git merge develop --ff-only
$ git push origin main

# Tag the release
$ git tag -s -a v1.0.0 -m "Release version 1.0.0"
$ git push origin v1.0.0
```

2. **GitHub Flow/Feature branching:** using one primary branch `main/master` and multiple `feature/*` branches. This is the branching strategy that I used for my personal projects where I'm the solo developer.

```sh
# create a feature branch
git checkout -b feature
echo "New shiny feature" > feature.txt
git add feature.txt
git commit -S -m "feat: add new feature"
echo "New shiny test" > test.txt
git add test.txt
git commit -S -m "test: add new test for feature"
# add more WIP commits here ...

# ======================================================================= #
# open a PR
$ gh pr create --base develop --editor --fill
# make some more commits to reflect code auditors' feedback

# everything is okay now, it's time to
# in the mean time, more commits are added to main branch
# make main local branch reflects remote branch
git checkout main
git fetch origin main
git rebase origin/main
# Then make feature local branch reflects remote branch
git checkout feature
git fetch origin feature
git rebase origin/feature
# Then make feature local branch reflects main local branch
git rebase main
# Finally, push the final change
git push --force-with-lease --force-if-includes origin feature
# Use the "Squash and Merge" option to create an atomic commit on top of main branch
# NOTE: Some people don't like squash merges WIP commits because they find values in ad-hoc commit messages that reflect the developers' design decisions.
# ======================================================================= #

# Sometimes a PR is not needed
# Squash merge via interactive rebase
git checkout main
git fetch origin main
git rebase origin/main  # overkill? nah just in case

git checkout feature
git rebase -i main   # change all `pick` to `s`/`squash`

git checkout main
git merge --ff-only feature
git push origin main
```

3. **Trunk-based:** all changes are made directly to `main/master` branch, use feature toggles, hotfix or other technologies to manage incomplete features.

4. **Release branch:** a `release` branch is created from the `main/master` branch to prepare a new release, then merged back into main branch once the release is complete.
   > IMO, we have tags for this use case.

### Step 4: Write automated test cases

> **NOTE:** The order of [Step 3](#step-3-write-automated-test-cases) and [Step 4](#step-4-implement-the-feature) can be swapped, if you are not a [Test-driven Development (TDD)](https://martinfowler.com/bliki/TestDrivenDevelopment.html) practitioner. However, using LLMs, TDD wasn't a hassle anymore, you can generate test cases first and ask LLMs to iterate against the test.

Features should be accompanied by automated tests to not only verify the reliability of the implementation through unit tests but also ensure existing functionality remains intact through regression testing.

_**SIX** Pros and practices:_

1. **Test-included vs Test-driven Development:** Tests don't have to exist before implementation, but tests must be bundled together with docs and implementation inside a commit.
1. **The sooner, the better:** Every new project must include a testing framework. Adding new test cases to an existing test suite is easier than creating a whole test suite from scratch.
1. **Old features shouldn't depend on new features:** Hide the implementation (e.g. by using `git stash`), then run the tests. They should be failed.
1. **Always be suspicious**: If a new test passes the first time, delibrately break the test and run it again to make sure it fails, then change it back again.
1. **Replicate production error locally:** Only by replicating the error then engineers can work on it.
1. **Enforce writing test through code review system:** GitHub PRs from external contributors must include tests in order to be merged.

### Step 5: Implement the feature

A single change on one "thing". A "thing" is a relatively vague concept, what it meant can differ in a case-by-case basis, and that change can be documented.

### Step 6: Update documentation

Explain the logic of the new implementation, how to run it, ... A feature isn't documented is a feature that doesn't exist.

_**SIX** pros and practices:_

1. **Start small, then scale:** For small projects, start by writing a single `README.md` with table of contents. README gets displayed on GitHub and PyPI. For bigger projects, keeps `README.md` simpler and use dedicated docs frameworks to write **versioned documentation**. These frameworks can provide a live reloading local server feature so you don't have to wait until deployment to see the changes.
1. **Up-to-date**: Docs and implementation must live under a single roof. By doing so, you can ensure the docs is up-to-date with the implementation. If docs is out of date, it will result in people losing trust in your project. They eventually will stop reading it and stop contributing to it as well.
1. **Versioned:** docs should have their own versioning system instead of only keeping up-to-date version. Docs framework can setup docs versioning easily.
1. **Tested:** docs should have its existance tested by unit tests.
1. **Reviewed:** docs should be included in a GitHub PR to check if it reflects the changes in implementation.
1. **End-user facing**: i.e. screenshot should be up-to-date as well. However it's a lot of work and real benefiters are non-tech users who can't read documentation.

### Step 7: Create a Perfect Commit

An **atomic commit** is a commit with a clear boundary of what it's changing. Each commit does one and only one simple thing and can be summed up in one simple short sentence, regardless of the amount of code change (1 letter or 100k+ LoC).

A **Perfect Commit** defines the **FOUR** crucial components of an atomic commit: tests, implementation, documentation and a semantic commit message containing a link to GitHub Issue.

To maintain a commit history full of Perfect Commits, a branching strategy must be determined at the beginning of the project.

To read more about Semantic Commit Message, I've written a dedicated TIL [here](./semantic-commit-message.md).

_**SIX** pros and practices:_

1. **Atomicity:** Avoid unrelated changes.
   ```sh
   git diff
   # avoid `print()` for quick debug
   git diff | grep 'print'
   ```
1. **Semantic commit message:** Follow the rules of Conventional Commits specification (extended with Angular convention).
1. **Flexibility:** Either commit all tests, implementation and docs at once, or making multiple WIP commits in a self-closed GitHub Pull Request then squash-merge them into a single Perfect Commit. There are commits to fix type, fix bugs (it depends) which isn't categorized as Perfect Commit.
1. **Releasable:** Commits must be "completed", i.e. the test suite passed. Keep the `main` branch releasable at all times and incomplete work stay in develop/feature branches. A non-working commit prevent the use of `git bisect` - a very important tool to track the commit that introduce a bug from an old codebase with thousands of commits.
1. **Reversible:** Rollbacks are do-able.
1. **Linear commit history:** Commits follow a straight line without any merge commits or branching paths.

_**FOUR** code audit practices:_

1. **Create pull request frequently:** It's best to prevent your feature branch from being out-of-date for too long to keep the merge conflicts as small as possible.
1. **Faciliate auditing pull request:** Since there is a clear boundary, anyone without prior knowledge about your code will have an easier time reading.
1. **Switch commentary to pull request:** Switch ongoing commentary to comments on pull request opened when opening a PR.
1. **Preview pull request:** Reviewing is a lot of easier if code auditors can try out the changes instead of only looking at code without actually running it.

### Step 8: Push out a release and create release note

After making the perfect commit:

- Update existing changelog file (`CHANGELOG.md`)
- Adding a release note that includes the relevant issues and their numbers.
- Update existing `setup.py` by incrementing the version number. The version follows Semantic Versoning (SemVer).
- Extracting the issue numbers list (Simon's [Observable notebook](https://observablehq.com/@simonw/extract-issue-numbers-from-pasted-text)).
- Ship a commit that bundles the new changelog with a commit message include the bumped version number and the issue numbers list.

```sh
# Example
git commit -m "Release 3.21

Refs #348, #364, #366, #368, #371, #372, #374, #375, #376, #379"
```

- Write release notes directly on GitHub Web UI by clicking "New Release" form and submit.
- GitHub Actions will be triggered automatically.

### Step 9: Provide a live demo (optional)

When possible, host a live demo. This is easy to do with web applications. Include a link to that live demo into the issue thread.

### Step 10: Tell the world about it

Share what you've done, beyond the people who read the release notes.

The platform where you share is depended on the size of the feature:

- Small: social media (Twitter/X, Facebook, ...) with screenshots and a link to the live demo.
- Large: annotated release notes, your blog, your weekly newsletter, ...
- New trick while building a feature: TIL. Remember to link to the new TIL from the issue thread.

## Reference

- [Best practices for repositories, GitHub Docs](https://docs.github.com/en/repositories/creating-and-managing-repositories/best-practices-for-repositories)
- [qoomon/conventional-commits-cheatsheet](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13#types)
- ["How I build a feature", Simon Willison, 2022-01-12](https://simonwillison.net/2022/Jan/12/how-i-build-a-feature/)
- ["Software engineering practices", Simon Willison, 2022-10-01](https://simonwillison.net/2022/Oct/1/software-engineering-practices/)
- ["The Perfect Commit", Simon Willison, 2022-10-29](https://simonwillison.net/2022/Oct/29/the-perfect-commit/#not-all-perfect)
- ["Coping strategies for the serial project hoarder", Simon Willison, 2022-11-26](https://simonwillison.net/2022/Nov/26/productivity/)
