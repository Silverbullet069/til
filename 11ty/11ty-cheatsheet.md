# 11ty Cheatsheet

<!-- tl;dr starts -->

11ty is my go-to Static Site Generator for my web projects.

<!-- tl;dr ends -->

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

## SIX sources of data

Data is merged from **SIX** sources of data before the template is rendered. 11ty called this behavior **Data Cascade**.

These sources of data here are listed in the order **from lowest priority to highest**.

> [!CAUTION]
>
> It's crucial for a maintainer to open a random template, looks at a variable and know its data sources and its Data Cascading outcome.
> If not, your project will be extremely hard to maintain.

### 1. Global Data Files

They are files whose data is exposed to every template in 11ty project. The most common file type is `.json`.

```txt
// NOTE: refer to configuration file above
src/_data/userList.json         # data file in global data dir
src/_data/users/userList.json   # data file in a folder

// The content of src/_data/userList.json and src/_data/users/userList.json
["user1", "user2"]

// Available in any template
{% for i in userList %}
  ...
{% endfor %}

{% for i in users.userList %}
  ...
{% endfor %}
```

**Using JavaScript Data File instead of JSON:**

```js
// src/_data/studioList.js

import eleventyFetch from "@11ty/eleventy-fetch";

/**
 * Grabs the remote data for studio images and returns back
 * an array of objects
 *
 * @returns {Array} Empty or array of objects
 */
// NOTE: ESM syntax
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
    return items;
  } catch (err) {
    console.log(err);
    return [];
  }
}

// you can use GraphQL, expose env var, cache remote images, CSS fonts
```

### 2. Configuration API Global Data

Global data not only can be added as Global Data Files but also can be specified in `eleventy.config.mjs`, using `addGlobalData()` method.

**NOTE:** IMO, it's best used for plugins and avoided for user content.

```js
eleventyConfig.addGlobalData("myString", "myValue"); // literal value

eleventyConfig.addGlobalData("myDate", () => new Date()); // evaluated before setting the value to the data cascade // myDate is Date instance

eleventyConfig.addGlobalData("myFunction", () => {
  return () => new Date();
}); // myDate is a function that returns a Date instance

eleventyConfig.addGlobalData("myNestedObject.myString", "myValue"); // literal value,  complex paths

eleventyConfig.addGlobalData("eleventyComputed.myString", () => {
  return (data) => "This is a string!";
}); // using this API with Computed Data, myString’s value will be "This is a string!"

eleventyConfig.addGlobalData("myFunctionPromise", () => {
  return new Promise((resolve) => {
    setTimeout(resolve, 100, "foo");
  });
}); // promise

eleventyConfig.addGlobalData("myAsyncFunction", async () => {
  return Promise.resolve("hi");
}); // async
```

### 3. Front Matter Data in Layout Template Files

Next data source is front matter data in Layout Template files, commonly specified inside `src/_includes/layout` directory.

```html
---
<!-- src/_includes/layout/base.html -->
title: My Rad Blog
---

<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{{ title }}</title>
  </head>
  <body>
    <!-- The Layout Template will populate the `content` data with Leaf Template's `content` -->
    {{ content | safe }}
    <!-- avoid double-escape the output, since {{content}} will be escaped again by the Leaf Template who used this Layout Template -->
  </body>
</html>
```

> **NOTE:** IMO, Front Matter Data in Layouts is best avoided for better maintainability. The fewer data sources there are, the simpler the application will be.

### 4. Template and Directory Specific Data Files (or Template/Directory Data Files)

Beside global data files, there will be time when you want the data to be available locally only to **ONE specific template** or **ONE specific directory of templates** by searching for JSON and JS file in specific places.

These templates are usually written in Markdown with front matter.

Example: template: `posts/subdir/my-first-blog-post.md`

- Highest: Template's front matter data
- High: Template Data Files
  - `posts/subdir/my-first-blog-post.11tydata.js` (highest, among the files)
  - `posts/subdir/my-first-blog-post.11tydata.json`
  - `posts/subdir/my-first-blog-post.json` (best practice)
- Normal: Directory Data Files
  - `posts/subdir/subdir.11tydata.js` (highest, among the files)
  - `posts/subdir/subdir.11tydata.json`
  - `posts/subdir/subdir.json` (best practice)
- Low: Parent Directory Data Files

  - `posts/posts.11tydata.js` (highest, among the files)
  - `posts/posts.11tydata.json`
  - `posts/posts.json` (best practice)

    ```jsonc
    // Apply a default layout and permalink to multiple templates
    {
      "layout": "layouts/post.njk",
      "permalink": "/post/{{ title | slugify }}/index.html"
    }
    ```

- Lowest: Global Data Files in `_data/*`

The name of the data files must match either the name of the template or the name of the directory it resides within. However, this behavior can be customized via ` eleventyConfig.setDataFileBaseName("index");` API.

It doesn't have to be `*.11tydata.*`, you can customize it via `eleventyConfig.setDataFileSuffixes()` API. But their priority will be lower than their JS/JSON counterparts.

### 5. Front Matter Data in Leaf Template File

Locally assigned front matter values in Leaf Template file override things further up the Data Cascade.

```html
<!-- prettier-ignore -->
---
title: My page title
permalink:          # can use variable and shortcodes
eleventyComputed:   # can use and set variable and shortcodes for other front matter
                    # fields to use.
---
<!DOCTYPE html>
<html></html>
```

### 6. Computed Data

This is the end of the Data Cascade.

<!-- TODO: there is limited use for it so I will skip it for now. -->

## Supplied Data

- `pkg`: the local project's `package.json` data.
- `pagination`: you can
  using the `pagination` key in front matter, this divides data into chunks for multiple output pages.
- `collections`: lists of all of your content, grouped by tags. Use dot notation (i.e. `collections.featuredWork`).
- `page`: has information about the current page.
- `eleventy`: contains 11ty-specific data from env vars.

## Permalinks

By default, this is the outputing behavior:

| Input                                                                           | Output                             | Href                |
| ------------------------------------------------------------------------------- | ---------------------------------- | ------------------- |
| `index.md`                                                                      | `_site/index.html`                 | `/`                 |
| `about.md`                                                                      | `_site/about/index.html`           | `/about/`           |
| `subdir/template.md`, `subdir/template/template.md`, `subdir/template/index.md` | `_site/subdir/template/index.html` | `/subdir/template/` |

Remap the template's output to a different path than the default, use the `permalink:` key in the template's front matter.

```yml
---
# basic example
permalink: "this-is-a-new-path/subdirectory/unexisted/"
permalink: "this-is-a-new-path/subdirectory/unexisted/index.html" # best practice
# => _site/this-is-a-new-path/subdirectory/testing/index.html
# NOTE: if a subdirectory does not exist, it will be created automatically.

# skip writing to the file system
permalink: false

# Nunjucks template syntax
title: This is a new path
permalink: "subdir/{{ title | slugify }}/index.html"
# => `_site/subdir/this-is-a-new-path/index.html`
# NOTE: always remember to put quotes, YAML parse anything start with {} as object

# special `page` variable
date: "2025-05-01"
permalink: "/{{ page.date | date: '%Y/%m/%d' }}/index.html"
---
```

Change permalinks for one directory:

```js
// context: a directory that contains multiple content templates, like `recipes/cookies.md`, `recipes/soup.md`, ... etc 50 more, either:
// - manually set a permalink in the fronmatter of each recipe (bad idea!)
// - dynamically generate the permalink inside a JS Directory Data File `recipes.11tydata.js`
export default {
  // the order of Data Cascade should have not made the `title:` field available in the Directory Data File
  // `permalink` is an exception of implied Computed Data, therefore have `title` available
  permalink: function ({ title }) {
    return `/recipes/${this.slugify(title)}`;
  },
};
```

Mapping one URL to Multiple Files for Internationalization (a.k.a i18n): Official documentation said to use server-side redirects, but I beg differ.

## Plugins

### RSS

### Internationalization (I18n)

This plugin provides **TWO** universal filters and **ONE** addition to `page` variable.

### Image

### Id Attribute

## Tips

- Include partials in templates to practice DRY.
- Local over Global installation: Eleventy suggests we install it locally. We run it via `npx`. When you work in a team, running packages locally means everyone is running off the same setup.
- Data can come from multiple places:
  - Inside `src/_data` directory
  - Collections (good for blog posts)
  - Front matter
  - Remote data
- A SSG that can work with remote data can turn itself into a front-end for a CMS.
- 11ty has clever set up for dates:
  - If there is no `date:`, and there is no date information in the file name, it will use the file's metadata (more specifically, file creation) in OS.
  - If there is no `date:`, and there is date informatin (e.g. `2025-01-01-foo-bar.md`), it will extract the date from there.
  - There are multiple ways to specify `date:`
    - `date: Last Modified`: resolve to the file's last modified date.
    - `date: Created`: resolve to the file's created date (this is what used if `date` is omitted)
    - `date: git Last Modified`: resolve to the file's latest git commit (besure to check in the file)
    - `date: git Created`: resolve to the file's first git commit.
    - `date: "2025-01-01"`: enclosed double quotes.
    - `date: 2025-01-01`: no double quotes.
