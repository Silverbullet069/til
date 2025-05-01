# How I implement Dark Mode feature for D2 Playground

<!-- tl;dr starts -->

Dark mode is my favorite feature in any software applications out there.

<!-- tl;dr ends -->

I selected this solution for the following advantages:

- Pure CSS, no need JS.
- DRY.
- Cross-platform.
- Simple, easy to understand.
- High flexibility, easy to make exception.

Copy/paste the following boilerplate:

```css
@media (prefers-color-scheme: light) {
  :root:not(.theme-dark):not(.theme-not-preferred),
  .theme-preferred {
    --media-prefers-light: ;
  }
  .theme-not-preferred {
    --media-prefers-light: initial;
  }
}

/* render as the opposite of the default root preferences */
.theme-not-preferred,
.theme-light {
  --media-prefers-light: ;
}
/* render based on the default root preferences */
.theme-preferred,
.theme-dark {
  --media-prefers-light: initial;
}

:root,
.theme-preferred,
.theme-not-preferred,
.theme-light,
.theme-dark {
  /* arbitrarily, dark by default */

  /* internal variables, shouldn't be used outside of this scope */
  /* const foo_bar_light = var(--media-prefers-light) && your_light_value */
  --theme_0_light: var(--media-prefers-light) 0 0% 100%;
  --theme_1_light: var(--media-prefers-light) 0 0% 0%;
  --theme_2_light: var(--media-prefers-light) hotpink;
  --theme_scheme: var(--media-prefers-light) light;

  /* const theme-var = maybe_light_val || your_dark_value */
  --theme-0: var(--theme_0_light, 0 0% 0%);
  --theme-1: var(--theme_1_light, 0 0% 100%);
  --theme-2: var(--theme_2_light, rebeccapurple);
  color-scheme: var(--theme_shceme, dark);
}
```

## References

[Jane Ori's "CSS Light/Dark Mode Implementation WITHOUT Duplicating Vars"](https://dev.to/janeori/css-lightdark-mode-implementation-without-duplicating-vars-22c9)
