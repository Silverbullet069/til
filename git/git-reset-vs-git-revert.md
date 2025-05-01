# Git Reset versus Git Revert

<!-- tl;dr is the summary of your TIL -->

I always forget about how these two commands work.

- `git revert`:

* makes a new commit
* changes the working directory's state to "the state that does not include the changes from the reverted commit."
* it is incorrect to say that it changes to the state of the previous commit of the reverted commit.
* preserve commit history

- `git reset`:

* point HEAD to a specific commit (HEAD is reference to the current commit on the currently checked-out branch).
* `--soft`: working directory stay the same.
* `--hard`: everything uncommitted will be removed, so it's best to use this option when `git status` is clean. If you have anything unfinished, just make a WIP commit.
* never delete commits **in not currently checked-out branch**. In practice, they're usually commits from feature branched which are merge to the currently checked-out branch
* unmonitored (not delete) commits from the commit that HEAD is currently pointed to the commits after the target commit **in currently checked-out branch**. To retrieve them use `git reflog` and once again use `git reset --hard` to go back.
* change commit history.

## References

- [Mark Longair's answer about `git reset --hard`](https://stackoverflow.com/a/9530204/9122512)
- [AD7six's answer about `git revert`](https://stackoverflow.com/a/19032678/9122512)
- [Jonathan.Brink's answer about the removal of commit history after using `git reset --hard`](jhttps://stackoverflow.com/a/51863814/9122512)
