# Process Substitution vs Pipelining in Shell Scripting

<!-- tl;dr starts -->

When I was reading [triffid/pia-wg#pia-wg.sh](https://github.com/triffid/pia-wg/blob/master/pia-wg.sh), I found a lot of `< <()` syntax. What does it do?

<!-- tl;dr ends -->

## Input substitution

There are two distinct ways to provide a file to a command:

1. Direct file argument: `[command] file`

- Passes the actual file reference.
- Command receives file path as argument.

2. Input redirection: `[command] < file`

- Passes file content via _stdin_, a.k.a standard input.
- Command receives data stream.

> Example:
>
> ```bash
> # Using file argument
> cat test.txt
>
> # Using input redirection
> cat < test.txt
> ```

`<` syntax is _input redirection_. Shell opens the input file and write its contents to the standard input of another process.

> Analogy: a baby and an adult drinking water:
>
> - An adult can open the tap and fill a glass (open the file => read its content)
> - However, a baby can only be given water directly (can't open file, only process content)

Some notable cases:

- There is no easily perceived difference between `cat file` and `cat < file`since `cat` can work with both file and content.
- There is no knowledge about files in `tr`, so `<` must be used.
- Some programs like `wc` when given a FILE as argument will also print filename, but if given stream, no filename is printed (or print `-` like `md5sum`).

## Process substitution

`<()` is _process substitution_, just like `$()` is command substitution.

Process substitution is used when data originally not coming from a file is put into an anonymous file (a file descriptor) so the command can read from it. In another way, it eliminates the process of writing data into a temporary file, more so if the data isn't meant to be put inside file and had to be deleted later.

Input redirection is used simultaneously with Process substitution to mimic the behavior of stream a file's content to command.

> Example:
>
> ```sh
> # Print file descriptor
> echo <(echo "Hello World") # /dev/fd/63
>
> # Read content from a file
> cat <(echo "Hello World") # Hello World
> wc -l <(echo "Hello World") # 1 /dev/fd/63
>
> # Read content from a stream
> cat < <(echo "Hello World") # Hello World
> wc -l < <(echo "Hello World") # 1
> # echo "Hello World" | wc -l
> ```

## When to use which?

- Pipelining, or streaming using `|` syntax makes it easy to read for linear operation, also achieve memory efficient when processing large files.
- Process substitution, on the other hand, should be used when command needs to handle multiple inputs/outputs simultaneously, and the inputs are coming from temporary files which are created by other commands.

**NOTE**: do not use process substitution when you're processing large file.
