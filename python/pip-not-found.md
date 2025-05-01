# Sometimes `pip` not found inside `venv` virtual environment

<!-- tl;dr starts -->

Happens everytime I tried to create a `.venv` virtual environment from inside VSCodium Flatpak `bash` console.

<!-- tl;dr ends -->

Run `python -m ensurepip`, credit to [kainjow](https://stackoverflow.com/a/56896098).

> NOTE: sometime, Python virtual environment have multiple Python versions, and `ensurepip` install `pip` that will associate with the current activated version.
