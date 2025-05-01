# Templating and Development environments

<!-- tl;dr starts -->

Refrain from doing everything from scratch.

<!-- tl;dr ends -->

## Templating

Your most optimized project directory structure with prepopulated files that can setup your development environment in the blink of an eye.

_Pros and Practices:_

- **Minimalism:** Don't install unnecessary packages.
- **Flexibility:** For microservices, a new template is inevitable. For monorepo, there are elements with similar structures - components and feature implementations that can be reused.
- **Up-to-date**: Make sure they're used constantly.

_Python tech stack:_

- Project templates: [cookiecutter](https://cookiecutter.readthedocs.io/en/stable/) (for Python) and GitHub template repositories.
- CLI framework: Click
- CI/CD: GitHub Actions
- Virtual environment: `python venv`
- Documentation: `README.md`, [Read the Docs](https://readthedocs.org/), [Sphinx](https://www.sphinx-doc.org/) + [reStructuredText](https://www.sphinx-doc.org/en/master/usage/restructuredtext/basics.html)/[MyST](https://myst-parser.readthedocs.io/) + [sphinx-autobuild](https://github.com/executablebooks/sphinx-autobuild) (host local docs server)
- Linter: `autopep8`.
- Formatter: `black`.
- Test framework: `pytest`.

_Examples:_

```sh
# runs entire test suite but quits at the 1st test that fails
pytest -x

# re-runs any tests that failed during the last test run
pytest --lf

# open the Python debugger at the first failed test, omit -x to open it at every failed test
# Simon W add `assert False` to get a shell inside the test to interact with objs, then
# figuring out how to best run assertions again them
pytest -x --pdb
```

> Simon Willison has 3 Cookiecutter templates, 1 for library, 1 for command-line tool, 1 for Datasette plugins.

## Tested, automated process for development environment

Beside the right directory structure, a README and a test suite with a single, dumb passing test, you will need to install the necessary dependencies to start working on features.

_Pros and practices:_

- **Documentation**: not just the code that realized your features but the scripts that made up your development environments are also in need of being documented, especially if you're working in a team.
- **Local containerized solution:** building Dockerfile or Docker Compose file.
- **Cloud-based solution:** click a button on a web page and have a fresh, working development environment running a few seconds later. E.g. Gitpod, ...
