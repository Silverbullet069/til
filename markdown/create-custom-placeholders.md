# Create Custom Placeholders to Dynamically Process and Fill Automatically

<!-- tl;dr start -->

When I was building logic for [update_readme.py]() script that automatically update [README.md file]() of [my TIL]() whenever there is a new commit on the GitHub Repository. I've come across a method to both process and populate data dynamically: adding custom placeholders

<!-- tl;dr end -->

This is the simplify template of my README.md file:

```md
# TIL

## Introduction

foo foo foo...

<!-- count starts -->{}<!-- count ends --> TILs so far.

## FAQ

bar bar bar...

## Table of Contents

<!-- toc starts -->

...

<!-- toc ends -->

<!-- index starts -->

...

<!-- index ends -->
```
