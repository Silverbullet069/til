# 11ty Cheatsheet

<!-- tl;dr starts -->

11ty is my go-to Static Site Generator for my web projects.

<!-- tl;dr ends -->

Eleventy is a coordinator, between the templates and the data processing through these templates. The template can be Markdown, Nunjucks, HTML, ... and the data can be inside dedicated JSON and JS snippets, the template file's frontmatter, ...

## Directory structure

> Always start by designing your directory structure.

```txt
_site/                                # files that will be served on production
admin/                                # Decap CMS admin directory, no `npm` module
│   |-- index.html
│   |-- config.yml
functions/                            # file-based routing Cloudflare Pages Functions
|   |-- [foo].js
|   |-- bar.js
|   |-- baz/
src/
│   |-- _11ty/                        # Configuration files and logic for Eleventy
│   │   |-- collections/              # Collection definitions (e.g., for multilingual content)
│   │   │   |-- foo_en.js
│   │   │   |-- foo_vi.js
│   │   |-- filters/                  # Pure functions that modify A to B
|   |   |   |-- date.js
│   │   |-- utils/                    # General pure functions
|   |   |   |-- sort.js
│   │   |-- shortcodes/               # Template Language Custom Tags wrapper, rarely used in small project
│   |-- _data/                        # Global data files (JSON/JS)
│   │   |-- foo.json
│   │   |-- bar.js
│   │   |-- ...
│   |-- _includes/
│   │   |-- layouts/                  # Layout templates (Nunjucks)
│   │   │   |-- feed.html
│   │   │   |-- ...
│   │   |-- macros/                   # Nunjucks macros
│   │   |-- partials/                 # Reusable components (e.g., header, footer)
│   |-- assets/
│   │   |-- fonts/                    # .ttf
│   │   |-- imgs/
│   │   │   |-- foo/                  # images for src/content/{{locale}}/foo/
│   │   │   |-- bar/                  # images for src/content/{{locale}}/bar/
│   │   │   |-- favicon.ico
|   |   |   |-- icon.svg
│   │   |-- css/                      # stylesheets (.css, .scss, .sass, ...)
│   │   |-- js/                       # external JavaScript files (local CDN, ...)
│   │   |-- robots.txt
│   |-- content/                      # content that managed by a Git-based CMS
│   |   |-- vi/                       # multilingual projects
│   |   |-- en/
|   |   |   |-- pages/                #
|   |   |   |-- links/
|   |   |   |-- foo/
|   |   |   |   |-- foo.11tydata.js   # export `layout:` and `permalink:`
|   |   |   |-- bar/                  # same as "foo/"
|   |   |   |-- en.11tydata.js        # export locale: "en"
|   |   |-- index.njk
|   |   |-- sitemap.njk               #
│   |-- rss.html                      # RSS feed template
build_tasks/
|
eleventy.config.mjs
jsconfig.json
```

## Configuration file

```js
// plugins
import eleventyRssPlugin from "@11ty/eleventy-plugin-rss";
import { I18nPlugin } from "@11ty/eleventy";

// internal modules
import { sortByDisplayOrder } from "./src/utils/sort.js";
import dateFilter from "./src/filters/date-filter.js";
import w3DateFilter from "./src/filters/w3-date-filter.js";

// Add TypeScript Type Definitions, which enable some extra autocomplete features in IDE
/** @param {import("@11ty/eleventy").UserConfig} eleventyConfig */
export default function (eleventyConfig) {
  // CAUTION: Order matters!

  // eleventyConfig.setDynamicPermalinks(false); // disable dynamic templating totally, this will disable save location customization. Might be a lot faster.

  // Plugins
  eleventyConfig.addPlugin(eleventyRssPlugin);
  eleventyConfig.addPlugin(I18nPlugin, {
    // any valid BCP 47-compatible language tag is supported
    defaultLanguage: "", // Required, this site uses "en"

    // Rename the default universal filter names
    filters: {
      // transform a URL with the current page’s locale code
      url: "locale_url",

      // find the other localized content for a specific input file
      links: "locale_links",
    },

    // When to throw errors for missing localized content files
    errorMode: "strict", // throw an error if content is missing at /en/slug
    // errorMode: "allow-fallback", // only throw an error when the content is missing at both /en/slug and /slug
    // errorMode: "never", // don’t throw errors for missing content
  });

  // cre: https://www.11ty.dev/docs/languages/nunjucks/#nunjucks-environment-options
  eleventyConfig.setNunjucksEnvironmentOptions({
    throwOnUndefined: true,
  });

  eleventyConfig.setInputDirectory("src"); // def: .
  // eleventyConfig.setIncludesDirectory("my_includes"); // def: _includes // rel to input dir
  // eleventyConfig.setLayoutsDirectory("_layouts"); // def: _includes // if set, the layouts will live outside of the Includes directory
  // eleventyConfig.setDataDirectory("lore"); // def: _data // rel to input dir
  // eleventyConfig.setOutputDirectory("dist"); // def: _site // rel to root dir

  // eleventyConfig.setQuietMode(true); // 11ty will not show each file it processes and the output file anymore // IMO, it's better use ad-hoc CLI option `--quiet`

  // eleventyConfig.setDataFileBaseName("index"); // by default, 11ty will look for Directory Data Files that match the current folder name. Use this setting if you want to name your files differently

  // eleventyConfig.setDataFileSuffixes([".11tydata", ""]); // file suffixes for Template and Directory Specific Data Files
  // *.11tydata.json, *.11tydata.js, *.json

  // eleventyConfig.setFrontMatterParsingOptions({ language: "js" }); // set the syntax that would be used in your front matter // def is YAML

  /* ===================================================================== */
  /* Passthrough                                                           */
  /* ===================================================================== */
  // Specify files or directories to be copied into output directory
  eleventyConfig.addPassthroughCopy("admin"); // Decap CMS directory
  eleventyConfig.addPassthroughCopy("src/images/"); // Static assets // NOTE: rel to root dir
  // eleventyConfig.addPassthroughCopy("**/*.jpg"); // glob pattern, maintain directory structure
  // eleventyConfig.setTemplateFormats(["md", "css"]); // def=html,liquid,ejs,md,hbs,mustache,haml,pug,njk,11ty.js // css is not yet a recognized template extension in Eleventy
  eleventyConfig.setServerPassthroughCopyBehavior("passthrough"); // def="copy", files are referenced directly and will not be copied to your output directory. Changes to passthrough file copies WILL NOT trigger an 11ty build but will live reload appropriately in the dev server

  // structured content at a collection level
  eleventyConfig.addCollection("work", (collection) =>
    sortByDisplayOrder(collection.getFilteredByGlob("./src/work/*.md"))
  );
  eleventyConfig.addCollection("featuredWork", (collection) =>
    sortByDisplayOrder(collection.getFilteredByGlob("./src/work/*.md")).filter(
      (x) => x.data.featured
    )
  );
  // why reverse it?
  // 11ty has sorted them in chronological date order
  // we want them to be sorted in reverse chronological, which means newest first
  eleventyConfig.addCollection(
    "blog",
    (collection) =>
      // create a copy of the orginal array and mutate it instead
      // in case we want to use our blog collection somewhere else in project and didn't want to order reversed
      [...collection.getFilteredByGlob("src/posts/*.md")].reverse()
    // NOTE: you can use Nunjucks filter `reverse` instead of using JS method
  );
  eleventyConfig.addCollection("people", (collection) =>
    collection
      .getFilteredByGlob("./src/people/*.md")
      // Markdown files are numbered files instead of named files
      // If stuff changes, content can be switched out without breaking URLs
      .sort((a, b) => (Number(a.fileSlug) > Number(b.fileSlug) ? 1 : -1))
  );

  eleventyConfig.addFilter("dateFilter", dateFilter);
  eleventyConfig.addFilter("w3DateFilter", w3DateFilter);
  // Tips: you can also add filter for specific templating languages, such as Nunjucks
  // eleventyConfig.addNunjucksFilter(...)

  return {
    // NOTE; order doesn't matter
    markdownTemplateEngine: "njk", // Markdown files run through this template engine before translating to HTML
    dataTemplateEngine: "njk",
    htmlTemplateEngine: "njk", // HTML files run through this template engine before translating to (better) HTML
  };
}
```

## [Nunjucks](https://www.11ty.dev/docs/languages/nunjucks/)

It's my go-to Template Engine when working with 11ty. Mozilla created it.

### Features

- Set `{% set variableName %}`, `{% set variableName = "value" %}`. **NOTE:** async not supported, use `{% setAsync %}` instead.
- Includes (abs + rel): `{% includes 'includes.njk' %}`, `{% includes './includes.njk' %}`
- Extends (abs + rel): `{% extends 'base.njk' %}` , `{% extends './base.njk' %}`
- Imports (abs + rel): `{% import 'macros.njk' %}`, `{% import './macros.njk' %}`
- Built-in Universal Filters: `{{ name | filterName }}`.
  - `url`: normalie abs paths in content
  - `slugify` (memoized): change all non-alphanumeric to hyphen
  - `log` : run `console.log` inside templates
  - `getNextCollectionItem/getPreviousCollectionItem`
  - `inputPathToUrl` (memoized): map a template input path to output URL
  - `renderTransforms`
- Custom filter:
  - Added using Configuration API `addFilter("filterName", function (value) { ... } )` and `addAsyncFilter("asyncFilterName", function (value, callback) { ... }`
  - Inside the callback function, 11ty allows access for specific data properties: `this.page`, `this.eleventy`, `this.env`, `this.ctx`.
  - Memoization supported: `addFilter("filterName", memoize((value) => { ... }))`.
  - Custom filter can be added per-engine using Configuration API: `addLiquidFilter()`, `addNunjucksFilter()` and their async counterparts.
- Custom Tags
- Shortcodes: reusable bits of content.

### Syntax

Use double curly braces syntax (now called "template syntax") to refer to variables, use ` ... | filterName` to apply filter.

```njk
{{ foo }}
{{ foo | bar }}
```

### Environment Options

```js
export default function (eleventyConfig) {
  eleventyConfig.setNunjucksEnvironmentOptions({
    throwOnUndefined: true,
  });
}
```

## [SIX sources of data](https://www.11ty.dev/docs/data/#sources-of-data)

Templates can retrieve data ("variable references") from **SIX** different sources at build time. When similar data exists in multiple sources, higher priority sources override lower priority sources. 11ty calls this behavior the [Eleventy Data Cascade](https://www.11ty.dev/docs/data-cascade/).

I have listed these sources of data in the order of **lowest to highest** priority:

IMO, this Data Cascade is hardest part to grasp in 11ty. One could render their own projects unmaintainable if the template's behavior is hard to understand due to the poor data sources' design decisions.

### 1. [Global Data Files](https://www.11ty.dev/docs/data-global/)

- Store static data or code, can be dynamically retrived during build.
- Every template can use them.
- File-based locator: use file/directory name with dot notation.

**Examples:**

1. Simple static JSON files

```sh
src/_data/goals.json          # JSON file
src/_data/users/goals.json    # JSON file in "users" directory
src/_data/data.json           # JSON file
```

`goals.json`

```json
[
  "Make personal website",
  "Draft blog post",
  "Rebuild personal website",
  "Write blog post",
  "Don't rebuild personal website"
]
```

`data.json`

```json
{
  "myData": ["item1", "item2", "item3", "item4"]
}
```

```html
<ul>
  {% for goal in goals %}
  <li>{{ goal }}</li>
  {% endfor %}
</ul>

<ul>
  {% for goal in users.goals %}
  <li>{{ goal }}</li>
  {% endfor %}
</ul>

<ul>
  {% for item in data.myData %}
  <li>{{ item }}</li>
  {% endfor %}
</ul>
```

2. Dynamic data from JS snippets

- Using `@11ty/eleventy-fetch` official plugin, data can be fetched remote once, and made available to all of the templates that referenced the JS data file's name (e.g. the filename becomes global variables `{{ studioList }}`). JS data files refer to each other using `this` keyword (e.g `this.studioList`)
- `eleventyFetch()` function caches the API responses for 1 day, improve build performance.
- During build process, 11ty auto calls exported function.
- Return empty array on failure, prevent template crash.
- Parameter `configData`: access 11ty's built-in global variables.

`src/_data/studioList.js`:

```js
import eleventyFetch from "@11ty/eleventy-fetch";

/**
 * Grabs the remote data for studio images and returns back
 * an array of objects
 *
 * @returns {Array} Empty or array of objects
 */
// I will ESM syntax
export default async function (configData) {
  // access configData.eleventy global variable
  // ...

  try {
    let url = "https://11ty-from-scratch-content-feeds.piccalil.li/media.json";
    const { items } = await eleventyFetch(url, {
      // set cache duration to 1 day
      duration: "1d",
      // Eleventy Fetch parse JSON
      type: "json",
    });

    // Pay attention to the data structure of this function's output
    return items;
  } catch (err) {
    console.log(err);
    return [];
  }
}

// you can use GraphQL, expose env var, cache remote images, CSS fonts, ...
```

### 2. [Global Data from the Configuration API](https://www.11ty.dev/docs/data-global-custom/)

> [!TIP]
>
> This is useful plugins, not recommended for app's content.

- Specify data inside `eleventy.config.mjs`
- Useful for plugins.
- Generic Global Data: `addGlobalData()`
- Per-engine Global Data: `addNunjucksGlobal()`

```js
// literal value
eleventyConfig.addGlobalData("myString", "myValue");

// evaluated before setting the value to the data cascade
// myDate is Date instance
eleventyConfig.addGlobalData("myDate", () => new Date());

// myDate is a `function` that returns a Date instance
eleventyConfig.addGlobalData("myFunction", () => {
  return () => new Date();
});

// literal value, complex paths
eleventyConfig.addGlobalData("myNestedObject.myString", "myValue");

// Computed Data - the highest priority source of data
// myString’s value will be "This is a string!"
eleventyConfig.addGlobalData("eleventyComputed.myString", () => {
  return (data) => "This is a string!";
});

// Promise
eleventyConfig.addGlobalData("myFunctionPromise", () => {
  return new Promise((resolve) => {
    setTimeout(resolve, 100, "foo");
  });
});

// async
eleventyConfig.addGlobalData("myAsyncFunction", async () => {
  return Promise.resolve("hi");
});
```

### 3. [Front Matter Data in Layout Templates](https://www.11ty.dev/docs/layouts/#front-matter-data-in-layouts)

- Anything duplicated among the Pages goes inside Layout Templates. Duplicates among low-level Layout Templates can be put inside high-level Layout Templates (11ty called it [Layout Chaining](https://www.11ty.dev/docs/layout-chaining/))
- By default, the Layout Template's extension is `.html` and placed inside `src/_includes/layouts/*.html`.
- Layout Template's frontmatter data can be merged with Page's frontmatter data, Page's frontmatter data have higher priority.
- Layout Template's frontmatter data can specify some [special data keys](#special-data-keys) that would prove useful for all Pages, use `layout:` allow one Layout Template using other Layout Template.

> [!NOTE]
>
> The closer to the content, the higher the priority the data.

> [!TIP]
>
> Frontmatter data in Layout Templates is best avoided for better maintainability. The fewer data sources there are, the simpler the application will be.

**Examples:** Layout Template: `src/_includes/layout/base.html`

```html
---
title: My Awesome Blog
---

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{ title }}</title>
  </head>
  <body>
    <!-- 'content' is replaced with the content of lower-level templates whose layout is this file -->
    <!-- avoid double-escape the output. 'content' from lower-level templates has already been properly escaped -->
    {{ content | safe }}
  </body>
</html>
```

### 4. [Template and Directory Specific Data Files](https://www.11ty.dev/docs/data-template-dir/)

- Global data is good, but sometimes you want to the data to be available locally to **ONE specific template** or **ONE specific directory of templates**.
- These Pages are commonly written in Markdown with front matter.
- JavaScript data file has the highest priority.
- The name of the data files must match either the name of the template or the name of the directory it resides within (as shown in Highest and High examples)
  - Change behavior with `eleventyConfig.setDataFileBaseName("index");` API

**Example:** list available data in Page `src/posts/subdir/my-first-blog-post.md`

- Highest: the Page's front matter data
- High: Data Template Files, applies to only `src/posts/subdir/my-first-blog-post.md`
  - `src/posts/subdir/my-first-blog-post.11tydata.js` (highest, among the files)
  - `src/posts/subdir/my-first-blog-post.11tydata.json`
  - `src/posts/subdir/my-first-blog-post.json` (best practice)
- Normal: Data Directory Files, applies to all Pages in `src/posts/subdir/*`
  - `src/posts/subdir/subdir.11tydata.js` (highest, among the files)
  - `src/posts/subdir/subdir.11tydata.json`
  - `src/posts/subdir/subdir.json` (best practice)
- Low: Data Parent Directory Files, applies to all Pages in `src/posts/**/*`

  - `src/posts/posts.11tydata.js` (highest, among the files)
  - `src/posts/posts.11tydata.json`
  - `src/posts/posts.json` (best practice)

    ```jsonc
    // Apply a default layout and permalink to multiple Pages inside `src/posts/**/*`
    {
      "layout": "layouts/post.njk",
      // custom permalink required ending with `/index.html` to prevent 11ty creating a plaintext file whose name is the title after being slugified
      "permalink": "/post/{{ title | slugify }}/index.html"
    }
    ```

- Lowest: Global Data Files in `_data/*`

### 5. [Front Matter Data in Page File](https://www.11ty.dev/docs/data-frontmatter/)

- Page's frontmatter fields override things further up the Data Cascade.
- Using `gray-matter` package, three types of front matter can be processed:
  - `---json` JSON frontmatter
  - `---js` JS frontmatter
  - `---` YAML frontmatter (the most common)
- There are some [special data keys](#special-data-keys) that can be specified inside Page's frontmatter.

> [!IMPORTANT]
>
> Nowadays bobody creates Page from scratch. They are created by Content Management System with arbitrary set of frontmatter fields. Therefore, developers should build their Page around these sets.

```yml
---
title: My page title
# TWO special frontmatter keys
# this change where the file goes on the file system
permalink: # can use variable and shortcodes
eleventyComputed: # can use and set variable and shortcodes for other front matter
---
<!DOCTYPE html>
<html></html>
```

### 6. [Computed Data](https://www.11ty.dev/docs/data-computed/)

- Leverage the special data key `eleventyComputed`.
- `eleventyComputed` is best specified inside **JS frontmatter** and/or **JS Data Global/Template/Directory File**

```js
export default {
  eleventyComputed: {
    myTemplateString: "This is a template string.",
    myString: (data) => "This is a string!",
    myFunction: (data) => `This is a string using ${data.someValue}`
    myAsyncFunction: async (data) => await someAsyncThing(),
    myPromise: (data) => {
      return new Promise((resolve) => {
        setTimeout(() => resolve("Delayed 100ms"), 100)
      })
    }
  }
}
```

**Examples:**

1. Create a navigation menu for your site using [Navigation plugin](https://www.11ty.dev/docs/plugins/navigation/)

- Prerequiiste: Navigation plugin relies on special data key `eleventyNavigation` that must be set inside EVERY individual Page file.
- Problem:
  - Pages is created by CMS has arbitrary set of frontmatter fields.
  - JSON Data Directory Files? It can only set default values yet `eleventyNavigation` must be set based on other data.
- Solution:

Page file: `src/posts/my-page-title.md` (and other `src/posts/*.md` file)

```yml
---
title: My Page Title
parent: My Parent Key
---
```

JS Global Data File: `src/_data/eleventyComputed.js`

```js
export default {
  eleventyNavigation: {
    // the `data` parameter holding all data that has been cascaded from the start
    // even `permalink` (this is a special case)
    key: (data) => data.title,
    parent: (data) => data.parent,
  },
};
```

JS Data Directory File + `eleventyComputed`: `src/posts/posts.11tydata.js`

```js
export default {
  eleventyComputed: {
    eleventyNavigation: {
      key: (data) => data.title,
      parent: (data) => data.parent,
    },
  },
};
```

The following data is automatically provied to Page files

```json
{
  // From Page's frontmatter, or lower-priority data sources in Data Cascade stack
  "title": "My Page Title",
  "parent": "My Parent Key",
  // From JS Data Directory File
  "eleventyNavigation": {
    "key": "My Page Title",
    "parent": "My Parent Key"
  }
}
```

If you don't want to use JavaScript, and the Page was manually created:

- Write YAML frontmatter fields directly for simplicity.
- Write JSON Data Directory files, remember to use the same template syntax.
- NOTE: "template syntax" is slower than using JavaScript. This is enough to switch to JavaScript entirely.

`src/posts/posts.json`:

```json
{
  "eleventyNavigation": {
    // template string syntax
    "key": "{{ title }}",
    "parent": "{{ parent }}"
  }
}
```

`src/posts/my-page-title.(md|njk)`

```yml
---
title: My Page Title
parent: My Parent Key
eleventyComputed:
  eleventyNavigation:
    # Template string
    key: "{{ title }}"
    parent: "{{ parent }}"
    # reust + overwrite
    title: "This is my new {{title}}"
---
```

## [Special data keys](https://www.11ty.dev/docs/data-configuration/)

### Overview

Among the SIX source of data, there are a few sources that use special data keys as data. These keys can be found inside **JSON data file** or **Markdown frontmatter**.

> [!IMPORTANT]
>
> All frontmatter keys aren't able to use template syntax, except `permalink`.

Common data keys:

- `permalink`: change the output target of the current template. Can use template syntax.
- `layout`: wrap current Page with a Layout Template found in `src/_includes` folder. DO NOT add prefix `src/_includes` folder.
- `pagination`: enable iterating over data, outputing multiple HTML files from a single Page fiie.
- `tags`: a single string, that identifies that a piece of content is part of a collection.
- `date`: override the default date (the file creation metadata on OS filesystem) to customize how the file is sorted in a collection. 11ty has clever set up for dates:
  - If there is no `date:`, and there is no date information in the file name, it will use the file's metadata (more specifically, file creation) in OS.
  - If there is no `date:`, and there is date informatin (e.g. `2025-01-01-foo-bar.md`), it will extract the date from there.
  - There are multiple ways to specify `date:`
    - `date: Last Modified`: resolve to the file's last modified date.
    - `date: Created`: resolve to the file's created date (this is what used if `date` is omitted)
    - `date: git Last Modified`: resolve to the file's latest git commit (besure to check in the file)
    - `date: git Created`: resolve to the file's first git commit.
    - `date: "2025-01-01"`: enclosed double quotes.
    - `date: 2025-01-01`: no double quotes.

Advanced data keys:

- `templateEngineOverride`: sometimes, a file needed to be processed differently.
- `eleventyComputed`: set a complex data values based on other values in the Data Cascade stack. The complex data values is the 6th and highest priority source of data: [Computed Data](#6-computed-data)
- `eleventyDataSchema`: validate data in the Data Cascade stack.
- `eleventyNavigation`: object used by Navigation plugins.
- `eleventyImport.collections`: ...
- `dynamicPermalink`: ...
- `permalinkBypassOutputDir`: ...

### Permalink

`permalink` data key allows remapping the template's output path to a different path than the default. By default, this is the outputing behavior:

<!-- prettier-ignore -->
| Input | Output | `<href="...">` |
| --- | --- | --- |
| `src/index.md` | `src/_site/index.html` | `/` |
| `src/about.md` | `src/_site/about/index.html` | `/about/` |
| - `subdir/template.md`<br/>- `subdir/template/template.md`<br/>- `subdir/template/index.md` | `_site/subdir/template/index.html` | `/subdir/template/` |

**Examples:**

1. Common syntax

```yml
---
# ============================================================================ #

# static permalink
permalink: "new-path/subdir/unexisted/"
permalink: "new-path/subdir/unexisted/index.html" # always end with /index.html at the end
# 11ty create non-existant subdir automatically
# Output target: _site/new-path/subdir/unexisted/index.html

# skip writing output file to the file system
permalink: false

# ============================================================================ #

# dynamic permalink
title: "New path"
permalink: "subdir/{{ title | slugify }}/index.html" # double quote! YAML parse everything wrapped inside `{}` as obj
# Output target:
# _site/subdir/new-path/index.html

# special `page` variable
date: "2025-05-01"
permalink: "/blog/{{ page.date | date: '%Y/%m/%d' }}/index.html"
permalink: "/posts/{{ page.date | date: '%Y/%m/%d' }}-{{ title | slugify }}/index.html"
# Refresh memory: `page.date` comes from `date` frontmatter, date in filename or file creation date in OS filesystem as fallback
# Output target: _site/2025/06/29/index.html
# Clean URL without .html: https://examples.com/2025/06/29/
---
```

2. A directory contains multiple high-level Layout Templates (e.g. `recipes/cookies.md`, `recipes/soup.md`, ... etc 50 more).

To set permalinks to all of them, manually set a `permalink:` frontmatter data is a bad idea, we need to populate `permalink:` data from **outside** of these files. We can do so by creating a JS Data Directory File:

`recipes/recipes.11tydata.js`:

```js
export default {
  // NOTE: `permalink` is an exception of implied Computed Data - the highest priority data source
  // NOTE: that explains why `permalink` have access to `title`
  permalink: function ({ title }) {
    return `/recipes/${this.slugify(title)}`;
  },
};
```

3. Map one URL to multiple files for Internationalization (a.k.a i18n)

<!-- TODO: come back to this after you have i18n use case -->

### Layouts

<!-- TODO: finish -->

### Pagination

Iterate over a data set and create multiple files from a single template. Pagination can only be specified inside a Layout Template's frontmatter.

Pagination can be made against an Array (most common), an Object. Data source can come from frontmatter data, local or global files.

List of properties inside `pagination` object:

```json
{
  "items": [], // array of current pags's chunk of data
  "pageNumber": 0, // current page number, zero-based indexed
  "hrefs": [], // array of all page's `<a href="...">`
  "href": {
    "next": "url", // <a href="...">Next Page</a>
    "previous": "url", // <a href="...">Previous Page</a>
    "first": "...", // self-explanatory
    "last": "..." // self-explanatory
  },
  "pages": [], // array of all chunks of paginated data
  "page": {
    "next": {}, // Data object for the next page
    "previous": {}, // Data object for the previous page
    "first": {}, // Data object for the first page
    "last": {} // Data object for the last page
  }

  // inside each of the above object are properties inside `page` data key
  // that I've specified in 11ty Supplied Data section above.
}
```

**Example:**

1. `src/paged.njk`:

```md
---
tags:
  - myCollection
pagination:
  # specify data set
  data: testdata
  # control the number of each chunk
  size: 1 
  // size 2
  # using pagintation.items is tedious
  # if size=1, it's alias for scalar value `pagination.items[0]`
  # if size>1, it's alias for Array `pagination.items`
  alias: wonder
  # Force generate one pagination output with empty chunk of items
  generatePageOnEmptyData: true
  # Reverse the data, output: `["item 4", "item 3"]` and `["item 2", "item 1"]`.
  # NOTE: Collection API can do this also
  reverse: true
  # remove values from paginated data, output: `["item 1", "item 2"]` and `["item 4"]`
  filter:
    - item3
  # by default, collections.myCollection will only add the first page if size > 1
  addAllPagesToCollections: true
testdata:
  - item1
  - item2
  - item3
  - item4
permalink: "different/{{ pagination.items[0] | slugify }}/index.html"
# better
permalink: "different/{{ wonder | slugify }}/index.html"
# if size: 2
permalink: "different/{{ wonder[0] | slugify }}/index.html"
---

You can use the alias in your content too {{ wonder[0] }}.
```

=> `size: 1`: `_site/different/item1/index.html`, `_site/different/item2/index.html`, ...
=> `size: 2`: `_site/different/item1/index.html`, `_site/different/item3/index.html`.

JS frontmatter:

```md
---js
{
  pagination: {
    data: "testdata",
    size: 2,
    // `before` callback, modify, filter, change the pagination data in general
    // NOTE: `before` run first, then `reverse: true`, then `filter:`
    before: function(paginationData, fullData) {
      // Template Functions
      let slug = this.slugify(fullData.title)
      return paginationData.map(item => `${slug}-${item} with a suffix.`)
    }
  },
  testdata: [
    "item1",
    "item2",
    "item3",
    "item4"
  ]
}
---
```

---

2. `src/_data/globalDataSet.json` and `src/paged.njk`

```json
{
  "myData": ["item1", "item2", "item3", "item4"]
}
```

```md
---
pagination:
  data: globalDataSet.myData
  size: 1
---

<ol>
<!-- beside `items` array, there are many more property inside `pagination` object -->
{% for item in pagination.items %}
  <li>{{ item }}</li>
{% endfor %}
</ol>

<!-- Default output behavior -->
<!-- _site/paged/index.html -->
<!-- _site/paged/1/index.html -->
```

3. Paging a Collection

11ty has a special data key called `tags` to group templates into a Collection data structure. 11ty can make pagination data out of Collection data.

`src/blog.njk`:

```md
---
pagination:
  data: collections.posts
  size: 6
  alias: posts
---

<ol>
{% for post in posts %}
  <!-- there are so much more properties inside `posts` and `post` -->
  <li><a href="{{ post.url }}">{{ post.data.title }}</a></li>
{% endfor %}
</ol>
```

### Collections (using `tags`)

> [!IMPORTANT]
>
> There are two ways to create an 11ty collection: `tags` special data key and `addCollection()` API inside 11ty's configuration files.

A Collection groups content:

- ONE piece content can be a port of MANY collections.
- ONE collection can contain MANY piece of contents.
- The collection are sorted ascending by default, use Nunjucks `... | reverse` filter

`collections` object data structure:

```json
{
  "post": [], // array
  "post-with-dash": [] // array
}
```

Each property inside `collections` is an array.

Each `item` in `collections.post` has the following data structure:

```json
{
  // backward compatibility: any property inside "page" are available
  // outside `page`, e.g. item.url, item.fileSlug, item.outputPath, ...
  // recommonded to use page.*
  "page": {
    "inputPath": "./test.md"
    // ...
    // everything inside `page` built-in global variables
  },
  "data": {
    "title": "",
    "tags": []
    // ...
    // all data that can be accessed inside this piece of content
  },
  // alias to "templateContent"
  "content": "Template body, processed, no frontmatter",
  "rawInput": "Template body, unprocessed, no frontmatter"
}
```

`src/myPost.md`

```md
---
title: My Title
# single tag
tags: post
# multi tags, single line
tags: ["post", "post-with-dash"]
# multi tags, multi line
tags:
  - post
  - "post-with-dash"
# exclude content from being added to EVERY collection
eleventyExcludeFromCollections: true
# exclude content from being added to `post` collection
eleventyExcludeFromCollections: ["post"]
---

This will not be available in `collections.all` or `collections.post`.
```

Inside any templates:

```html
---
# declare Collection dependency, inform relationship for smarter incremental builds
eleventyImport:
  collections: ["post"]
---

<ul>
  {% for post in collections.post %}
  <li>{{ post.data.title }}</li>
  {% endfor %}
  <!--  -->
  {% for post in collections['post-with-dash'] %}
  <li>{{ post.data.title }}</li>
  {% endfor %}
  <!--  -->
  {% for post in collections.all %}
  <li><a href="{{ post.url }}">{{ post.url }}</a></li>
  {% endfor %}
</ul>
```

Automatically generate Tag Pages, use pagination to automatically generate a template for each tag:

```md
---
pagination:
  data: collections
  size: 1
  # tag is an array holding the list of keys of the `collections` object
  # or, the list of tag names, the list of string
  alias: tag
  # decentrailized tag list + black list design
  filter:
    - foo
    - bar
# for size=1, tag is collections.items[0] or the tag name
permalink: "/tags/{{ tag | slugify }}"w
---

<h1>Tagged "{{ tag }}"</h1>

<ol>
<!-- accessing the tag  -->
{% set tagList = collections[ tag ] %}
{% for post in tagList | reverse %}
  <li><a href="{{ post.url }}">{{ post.data.title }}</a></li>
{% endfor %}
</ol>
```

Each Page introduce a new tag results in a new pagination page being created: `_dist/tags/new-tag/index.html`. This design allows tag to be decentralized and don't have to be maintained manually.

### Dates

<!-- TODO: finish this -->

## [Supplied Data](https://www.11ty.dev/docs/data-eleventy-supplied/#page-variable-contents)

A list of data keys that're either built-in or computed based on [special data keys](#special-data-keys). Can be referred to in any Layout Template or Page.

> [!TIP]
>
> The above keys are reserved keywords, don't create new data key with the same name

- `pkg`: the local project's `package.json` data.
- `pagination`: divide data into chunks for multiple output pages.
- `collections`: lists of all of your content, grouped by tags. Use dot notation (i.e. `collections.featuredWork`).
- `page`: has information about the current page
  - `url`: `false` if `permalink` set to `false`, else `/path/to/template/` (trailing slash!)
  - `inputPath`: path to original source file for the template (e.g. `./path/to/template/file.md`)
  - `fileSlug` : `inputPath` filename without file ext (e.g. `file`)
  - `filePathStem`: `inputPath` without file ext (e.g. `/path/to/template`)
  - `date`: JS Date() object, can be used to sort collections.
  - `outputFileExtension`: use as suffix to `filePathSteam` for custom file extensions (e.g. `html`)
  - `outputPath`: path to output file in output directory (e.g. `./_site/path/to/output/file.html`)
  - `templateSyntax`: which type of files are processed (e.g. `liquid, md`)
  - `rawInput`: the unparsed/unrendered plaintaxt content of current template (e.g. `<!DOCTYPE...`)
  - `lang`: only needed with i18n plugin.
- `eleventy`: contains 11ty-specific data from env vars.
  - `version`: 11ty version
  - `generator`: for use with `<meta name="generator"`
  - `env`:
    - `root`: abs path to the dir in which you run 11ty CLI command
    - `config`: abs path to config files
    - `source`: either `cli` or `script`
    - `runMode`: either `build`, `serve` or `watch`.
  - `directories`: root-relative normalized path
    - `input`: `./`
    - `includes`: `./_includes/` (default)
    - `data`: `./_data` (default)
    - `output`: `./_site` (default)

## Plugins

11ty has a long list of both Official and 3rd-party Community Plugins. Official plugins live under `@11ty` NPM organization and have its name prefixed with `@11ty/`

There are **NINE** official plugins that could prove useful.

1. Image

   - [Optimize multimedia delivery on the web](https://developer.mozilla.org/en-US/docs/Learn_web_development/Extensions/Performance/Multimedia).
   - Perform build-time image transformation,
   - Cache remote images locally.
   - Add `width` and `height` attributes.
   - Accept wide variety of image input types: `jpeg`, `png`, `webp`, `svg`, ... Does not rely on file extensions.
   - Output multiple image sizes, maintain original aspect ratio. Generate `srcset` attribute.
   - Output multiple formats: `jpeg`, `png`, `webp`, `avif`. Generate the most efficient HTML markup using `<img>` and `<picture`.
   - Fast: deduplicate in-memory and disk cache.
   - Robust, local-first: save remote images, prevent broken URLs (via `@11ty/eleventy-fetch`).
   - Install: `npm install @11ty/eleventy-img`
   - There are 5 different ways to use this plugin:
     - **Image HTML Transform**: start with this one
     - Image Data Files: use images to populate data in the Data Cascade.
     - Image JS API: low-level JS API works independently of 11ty.
     - Image Shortcodes: use universal shortcodes in Nunjucks, Liquid or 11ty.js templates.
     - Image WebC: use WebC component for WebC templates.

1. Fetch

   - A utility to fetch and cache network requests.
   - Install: `npm install @11ty/eleventy-fetch`

1. `<is-land>` for Islands Architecture

   - Smartly and efficiently load and initialize client-side components.
   - This plugin enabled a hybrid architecture: 95% SSG and 5% CSR.
   - Easy to add to existing components.
   - Zero dependencies.
   - Small digital footprint (`4.56 kB` minimized, `1.47 kB` with Brotli compression)
   - Not tightly coupled to any server frameworks or SSGs.
   - Support SSR frameworks: Svelte, Vue, Preact
   - Install: `npm install @11ty/is-land`

1. Internationalization (i18n)

   - Manage pages and linking between localized content on 11ty projects

1. RSS

   - Generate an RSS/Atom feed to allow others to subscribe to your content using a RSS feed reader.

1. Upgrade Helper

   - Update 11ty project between major version releases.

1. Syntax Highlighting

   - Code syntax highlighting using PrismJS without client-size JS.

1. Navigation

   - Create hierarchical navigation in 11ty projects, supported breadcrumbs.

1. Bundle

   - Create small plain-text bundles of code (HTML, CSS, JS, SVG, ...)

## Services

List of tech stacks that support Eleventy integration:

### Deployment and Hosting

- GitHub Pages
- GitLab Pages
- **Cloudflare Pages**: my current use.
- Cloudflare Workers Static (hardcore).

Some play really nice with 11ty's Official plugins. Cloudflare Pages preserves `.cache` directory that is used by [Eleventy Fetch](https://www.11ty.dev/docs/plugins/fetch/) plugin. So does GitHub Pages.

### CMS

CMS add a web-based interface to the site, tech and non-tech personnel can easily update the site on-the-go. 11ty is not tightly coupled to any specific CMS. 11ty works best with Headless CMS what share the same characteristics.

I use **Decap CMS**, a Headless, Git-based CMS solution:

- The data is version controlled.
- Works as-is with your existing deployment process (e.g. works with deploy preview)
- No data migration is needed if in the future you don't want to continue using Decap CMS.

## Tips

- Learn how to design a good template frontmatter, template body and data files.
- DO NOT put everything inside Page's frontmatter, use **Page's body** if you're going to rely on Markdown's format to style a large amount of text.
- Use `{{ ... | log }}` Universal Filter to debug.
- Keep your template DRY by deduplicating modules in `src/_includes/partials`. Design Partials is like design **functions**. They need to have parameter, to be pure and idempotent.
- An SSG working with remote data can turn itself into a front-end for a CMS.
- Read [Quick Tip](https://www.11ty.dev/docs/quicktips/) to learn some more best practices.
- `.html` will be Layout Template, `.md` will be Page.
- With the help of CMS, duplication is not a problem anymore and Data/Template Directory File might not needed.
- DO NOT modify Page's frontmatter data using text editor, it must be done via CMS.
