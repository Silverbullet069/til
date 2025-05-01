# Release Notes Best Practices

<!-- tl;dr starts -->

End-user will not read it, but the future you and contributors will.

<!-- tl;dr ends -->

## NINE practices

1. **Start writing them**.
1. **Provide links to associated issue thread**.
1. **Make sure people can link to the release notes for a version**.
1. **Include the date**.
1. **Break large note into multiple sections**.
1. **Emphasize the highlights**.
1. **Provide examples and screenshots**.
1. **Credit your contributors**.
1. **Let people know**.

## GitHub Releases and GitHub Actions

### GitHub Releases

- Create new release attached to tags, each release gets its own linkable page.
- Releases can be written in Markdown.
- Releases can attach binary builds, `.zip` or `.tar.gz` file of the repository at that tag.

### GitHub Actions

- Play nice with GitHub Releases API
- When a new GitHub Release is posted, trigger an action workflow.

## Reference

- [Simon Willison's Blog "Writing better release notes"](https://simonwillison.net/2022/Jan/31/release-notes/)
