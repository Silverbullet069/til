# How You Should Build A Feature?

<!-- tl;dr starts -->

When I first saw his way of building features that can boost productivity on hundreds of personal projects at the same time, I knew I have found my ultimate methodology.

<!-- tl;dr ends -->

### Step 1: Create a verson control repository from a template and set up the development environment

Start by creating a GitHub repository. To save time and effort, use **an existing template** or **create your own template** if the tech stack of the existing template does not align with yours.

_Examples:_

- [simonw/click-app](https://github.com/simonw/click-app)
- [simonw/python-lib](https://github.com/simonw/python-lib)
- [CodeStitchOfficial/Intermediate-Website-Kit-SASS](https://github.com/CodeStitchOfficial/Intermediate-Website-Kit-SASS)
- [rochacbruno/python-project-template](https://github.com/rochacbruno/python-project-template/)

These GitHub Repository templates whose dynamic content should be able to be populated by [GitHub Actions](https://simonwillison.net/2021/Aug/28/dynamic-github-repository-templates/).

Using VSCode's Code Snippet feature to add reusable code snippets. I recommended you extract from the cheatsheet of the tech of your stack.

### Step 2: Create an issue and research the problem

Everything starts with an issue thread on version control system. The issue contains multiple comments recording your research and real progress while you're working on the feature.

_**EIGHT** components in an issue:_

1. **Background:** the purpose/goal of the feature, the reason for the change, use case story, UI/UX requirement, ...
1. **State of play before-hand:** existing code snippets from similar features from similar tools and links to existing docs.
1. **Reference:** tech documentation, blog, forum Q&A, ... It's like capturing those loose information sources and turning them into knowledge.
1. **Design decision**: note down all of your design decisions
   - Pick top-down or bottom-up design.
   - Directory structure design.
   - Workflow diagram.
   - CLI `--help` design.
   - Database schema design.
   - ...
1. **Attempt:** code snippets illustrating potential designs and false-starts. Again, do not start coding right away to minimize # of iterations.
1. **Screenshot:** your product's UI before and after. Animated screenshots are prefered ([LICEcap](https://www.cockos.com/licecap/) or [QuickTime](https://support.apple.com/en-vn/106375)).
1. **Prototypes:** a Python REPL session, a block of HTML and CSS, ... anything that showcase the final decision.
1. **After closed**: a link to the updated documentation and a live demo of the new feature (optinally).

_**SIX** pros:_

- **Issue-driven:** The issue is the thing that comes first before everything else, thus solving the **blank-page** problem.
- **Issues over Commit messages:** Simon stated that he received a net increase in his overall productivity.
- **Asynchronous:** By recording your research and real progress, you can leave it there and pick up the work later. Next time you won't waste time researching again.
- **Scalability:** A simple feature may result in a single issue with one comment (usually opened and closed immediately with a small commit containing only a few lines of code), while a complex feature can span multiple issues with hundreds of comments and commits.
- **Bidirectional references**: Any commit can relate to an issue, likewise you can navigate from the issue to any related commits. The same applies to the relationship between release notes and issues.
- **Temporary and informal documentation:** Issues are written in conversational language and serve as commitment-free, informal documentation, making them easy to write. Most importantly, no one will be upset or confused if issue comments do not match the final implementation.

_**TWO** practices:_

- **DO NOT FORGET:** Inexperienced practitioners often start coding right away without conducting any research firsthand.
- **Archive issue threads:** maintained a SQLite database on cloud for all of the issues and their comments.

> IMO, issues resembles the history of features. Learning history always give us a better insight, it applies to a range of subjects beside computer science, such as physics, chemistry, biology and literature. **Design decision** is very crucial and they're often omitted in official documentation.

_Examples:_ Issue thread's title

```
Initial research (tag: research)
TOOL_NAME COMMAND_NAME command (tag: enhancement)
COMMAND_NAME tests failing (tag: bug)
Suggestion: blah blah blah
Design the blah blah blah
Research the blah blah blah
```

### Step 3: Write automated test cases

> **NOTE:** [Step 3](#step-3-write-automated-test-cases) and [Step 4](#step-4-implement-the-feature) can swap their orders if you aren't [Test-driven Development (TDD)](https://martinfowler.com/bliki/TestDrivenDevelopment.html) practitioners. However, with Generative AI, TDD wasn't a hassle anymore, you can generate test cases first and ask AI models to iterate against the test.

Features should be accompanied by automated tests to not only verify the reliability of the implementation through unit tests but also ensure existing functionality remains intact through regression testing.

_**SIX** Pros and practices:_

1. **Test-included Development vs Test-driven Development:** Tests don't have to exist before implementation, but tests must be bundled together with docs and implementation inside a commit.
1. **The sooner, the better:** Every new project must include a testing framework. Adding new test cases to an existing test suite is easier than creating a whole test suite from scratch.
1. **Old features shouldn't depend on new features:** Hide the implementation (e.g. by using `git stash`), then run the tests. They should be failed.
1. **Always be suspicious**: If a new test passes the first time, delibrately break the test and run it again to make sure it fails, then change it back again.
1. **Replicate production error locally:** Only by replicating the error then engineers can work on it.
1. **Enforcing test update through code review system:** GitHub PRs from external contributors must include test cases in order to be merged.

### Step 4: Implement the feature

A single change on one "thing". A "thing" is a relatively vague concept, what it meant can differ in a case-by-case basis, and that change can be documented.

### Step 5: Update documentation

Explain the logic of the new implementation, how to run it, ... A feature isn't documented is a feature that doesn't exist.

_**SIX** pros and practices:_

1. **Start small, then scale:** For small projects, start by writing a single `README.md` with table of contents. README gets displayed on GitHub and PyPI. For bigger projects, keeps `README.md` simpler and use dedicated docs frameworks to write **versioned documentation**. These frameworks can provide a live reloading local server feature so you don't have to wait until deployment to see the changes.
1. **Up-to-date**: Docs and implementation must live under a single roof. By doing so, you can ensure the docs is up-to-date with the implementation. If docs is out of date, it will result in people losing trust in your project. They eventually will stop reading it and stop contributing to it as well.
1. **Versioned:** docs should have their own versioning system instead of only keeping up-to-date version. Docs framework can setup docs versioning easily.
1. **Tested:** docs should have its existance tested by unit tests.
1. **Reviewed:** docs should be included in a GitHub PR to check if it reflects the changes in implementation.
1. **End-user facing**: i.e. screenshot should be up-to-date as well. However it's a lot of work and real benefiters are non-tech users who can't read documentation.

### Step 6: Commit the change with a Perfect Commit

The Perfect Commit is an _atomic commit_ that faciliate divide-and-conquor technique by divide one complex task into **FOUR** components: tests, implementation, documentation and a link to GitHub Issue.

> **Atomic Commit**: a commit with a clear boundary of what it's changing. Each commit does one and only one simple thing and can be summed up in one simple short sentence, regardless of the amount of code change (1 letter or 100k+ LoC).

_**SIX** pros and practices:_

1. **Atomicity:** Avoid unrelated changes.
   ```sh
   git diff
   # avoid `print()` for quick debug
   git diff | grep 'print'
   ```
1. **Semantic commit message:** Follow the rules of Conventional Commits specification (extended with Angular convention).
1. **Flexibility:** Either commit all tests, implementation and docs at once, or making multiple WIP commits in a self-closed GitHub Pull Request then squash-merge them into a single Perfect Commit. There are commits to fix type, fix bugs (it depends) which isn't categorized as Perfect Commit.
1. **Releasable:** Commits must be "completed", i.e. the test suite passed. Keep the `main` branch releasable at all times. Incomplete work stay in develop/feature branches.
1. **Reversible:** Commits should be reversible without introducing breakage.
1. **Linear commit history:** Commits follow a straight line without any merge commits or branching paths.

```sh
# create a feature branch
git checkout -b feature

# make changes and commit
echo "New shiny feature" > feature.txt
git add feature.txt
git commit -m "feat: add new feature"
# more commit here ...

# meanwhile, main has new commits.
# main:    A---B---C
#           \
# feature:   D---E

# local main branch reflects remote main branch
git checkout main
git pull

# rebase local feature branch according to local main branch
git checkout feature
git rebase main

# git rebase performs these steps
# 1. identify the common ancestor of feature and main branch => commit A
# 2. save the feature branch's commits (D, E) as temporary patches.
# 3. reset feature branch to match main (A, B, C)
# 4. replay feature branch commit on top of the new feature branch, now called D' and E'

# Result
# main:    A---B---C
#                   \
# feature:           D'---E'

# the rebased commits receive new SHA hashes.
# the commit dates of rebased commits are updated to the current time.

# NOTE: if the same file were modified in both branches, there might be merge conflicts during rebase.
# NOTE #2: Once feature branch has been pushed to a remote repository, rebasing can cause issues for collaborators, because it rewrites existing history.
git push --force-with-lease

# reflects local main branch with local feature branch
git checkout main
git merge feature --ff-only # fast-forward merge, no merge commit created
```

_**THREE** code audit practices:_

1. **Faciliate auditing pull request:** Since there is a clear boundary, anyone without prior knowledge about your code will have an easier time reading.
1. **Switch commentary to pull request:** Switch ongoing commentary to comments on pull request opened when merging feature branch to `main` branch.
   > TODO: I still don't know why Simon do this?
1. **Preview pull request:** Reviewing is a lot of easier if code auditors can try out the changes instead of only looking at code without actually running it.

### Step 7: Push out a release and create release note

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

### Step 8: Provide a live demo (optional)

When possible, host a live demo. This is easy to do with web applications. Include a link to that live demo into the issue thread.

### Step 9: Tell the world about it

Share what you've done, beyond the people who read the release notes.

The platform where you share is depended on the size of the feature:

- Small: social media (Twitter/X, Facebook, ...) with screenshots and a link to the live demo.
- Large: annotated release notes, your blog, your weekly newsletter, ...
- New trick while building a feature: TIL. Remember to link to the new TIL from the issue thread.

## Reference

- [qoomon/conventional-commits-cheatsheet](https://gist.github.com/qoomon/5dfcdf8eec66a051ecd85625518cfd13#types)
- [Simon Willison's Blog "How I build a feature"](https://simonwillison.net/2022/Jan/12/how-i-build-a-feature/)
- [Simon Willison's Blog "Software engineering practices"](https://simonwillison.net/2022/Oct/1/software-engineering-practices/)
- [Simon Willison's Blog "The Perfect Commit"](https://simonwillison.net/2022/Oct/29/the-perfect-commit/#not-all-perfect)
- [Simon Willison's 25-minute talk "Coping strategies for the serial project hoarder", 2022-11-26](https://simonwillison.net/2022/Nov/26/productivity/)
