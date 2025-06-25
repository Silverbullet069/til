# Bash Automated Testing System

<!-- tl;dr starts -->

I'm automating a lot of things inside my machine. In order to make them run reliably, I need to test them somehow. This is also contributing to my practice of [The Perfect Commit](https://simonwillison.net/2022/Nov/26/productivity/).

<!-- tl;dr ends -->

## Cheatsheet

```sh
# Run before the first test case of the first test file
setup_suite() {
  echo "${BATS_SUITE_TMPDIR}" # the tmp dir common to all tests of a suite. Could be used to create files required by multiple tests.
}

# Run after setup_suite(), before the first test case of a test file
setup_file() {
  echo "${BATS_FILE_TMPDIR}" # the tmp dir common to all tests of a test file. Could be used to create files required by multiple tests in the same test file.
}

# Run after setup_file(), before every test case inside a test file
setup() {
  echo "${BATS_TEST_TMPDIR}" # the tmp dir for each test. Could be used to create files required only for specific tests.
}

# Run after every test case inside a test file
teardown() { 
  :
}

# Run after the last test case inside a test file
teardown_file() {
  :
}

teardown_suite() {
  :
}

# function invoke_foo_with_a_non_existent_file_path { #@test
@test "Invoking foo with a non-existent" {

  run foo path/to/non/existent/file
  [[ "$status" -eq 1 ]]
  [[ "$output" == "foo: no such directory: path/to/non/existent/file" ]]

  # if the test focused on the exit status, use first arguments
  run -N foo path/to/non/existent/file  # expect exit status N=0-255, fail if otherwise
  # `run -0 foo` is the same as `run foo`
  run ! foo path/to/non/existent/file   # expect nonzero exit status (1-255), fail if command succeeds

  run -1 foo
  [[ "${lines[0]}" == "usage: foo <filename>" ]]

  # retain empty lines in ${lines[@]}
  run --keep-empty-lines foo

  # if a command is starts with -, prefix it with --
  run -- -foo-bar

  # if you want separate stdout/stderr
  run --separate-stderr foo

  # using library instead of [[ statement
  assert_output
  assert_failure
  # ...
}
```
