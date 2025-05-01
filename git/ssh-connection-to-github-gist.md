# SSH Connection to GitHub Gist

<!-- tl;dr starts -->

When writing your `~/.ssh/config`, make sure that both hosts: `github.com` and `gist.github.com` are specified.

<!-- tl;dr ends -->

If you're trying to contribute to a GitHub Gist but no success:

```sh
ssh -T git@gist.github.com
# git@gist.github.com: Permission denied (publickey).
```

It's because you haven't specified `gist.github.com` as one of the host inside `~/.ssh/config` file. Add it to your file as follow:

```conf
# ...

# Personal GitHub
Host github.com gist.github.com
  HostName %h
  User git
  IdentityFile ~/.ssh/[YOUR_PRIVATE_KEY]
  IdentitiesOnly yes

# ...
```

Recheck your SSH connection to `git@gist.github.com`

```sh
ssh -T git@gist.github.com
# Hi [USERNAME]! You've successfully authenticated, but GitHub does not provide shell access.
```
