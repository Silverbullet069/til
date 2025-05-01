# HTML Semantic Elements

<!-- tl;dr starts -->

While I was learning 11ty at this [site](https://learn-eleventy.pages.dev), I've learned quite a great deal about writing Semantic HTML. I would like to note them down.

<!-- tl;dr ends -->

The banner role is usually reserved for content such as brand, navigation and search:

```html
<header role="banner"></header>
```

You should only ever have one `<main>` element, and it makes sence to add it in a Base layout so every page can use it.

When there are tons of links above main content, when someone focuses to the `<main>` and hit `Tab`, their focus will be sent to the next focusable element inside it.

```html
<!-- id and tabindex allows the element to be "programmatically focused" -->
<!-- when someone clicks a link that goes to #main-content, the <main> element will be focused -->
<main tabindex="-1" id="main-content"></main>
```

When there are 2 or more `<nav>`, having an `aria-label` attribute will have assistive technology users understand the difference between them:

```html
<nav aria-label="Primary"></nav>
<!-- another nav -->
<nav></nav>
```

A logo can have `aria-hidden="true"` attribute on it if it's purely decorative and screen reader user doesn't need to know it's there. Using `focusable="false"` can prevent older screen readers from being able to focus it.

```html
<svg aria-hidden="true" focusable="false"></svg>
```

Aria role `aria-current="page"` tells screen reader users that this item's link is to the current page that they're on

```html
<a aria-current="page"></a>
```

CSS hook `data-state="active"` adds decoration to the item to show the user they're already in that bit of the site (or the current URL is the prefix of that URL). It won't confuse screen reader users:

```html
<a data-state="active"></a>
```
