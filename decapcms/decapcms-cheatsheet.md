# DecapCMS Cheatsheet

<!-- tl;dr starts -->

Decap CMS is my go-to CMS solution for building personal web projects, as mentioned in [My Ultimate Web Tech Stack](../0-misc/my-ultimate-web-tech-stack.md).

<!-- tl;dr ends -->

## Why I choose Decap CMS?

It is a Git-based, open-source, headless CMS.

- Store content along with code.
- Enable content versioning, content updates handling on cloud providers using CI/CD pipeline built by GitHub Actions.
- Framework-agnostic, can be used with any static site generator.
- Provide a web-based admin panel UI with robust editor and can be also be hosted alongside the main site.

## What is it actually?

At its core, Decap CMS is an open-source React application acting as a wrapper for the Git workflow, using GitHub, GitLab and Bitbucket API.

Hooking Decap CMS to your website is basically adding a content editor that can make commits to GitHub without touching the codebase nor running Git CLI commands.

_Pros:_

1. **Fast, web-based UI:** non-tech users can access the CMS on browser. It has rich-text editing, real-time preview, drag-and-drop media uploads.
2. **Easy installation:** you can drop-in a few files to the project root - admin panel UI and serverless functions - alongside your existing codebase.
3. **Modern authentication:** using GitHub, GitLab or Bitbucket JWT.
4. **Flexible content types:** support unlimited number of content types with custom fields.
5. **Fully extensible:** custom-styled previews, UI widgets, editor plugins.

## Releases

Decap CMS is released on 2 platforms:

1. **Package Manager:** `npm` and `yarn`.
2. **CDN:** add `<script src="https://unpkg.com/decap-cms@^3.0.0/dist/decap-cms.js">` tag into `admin/index.html`. It's recommended that you use `^3.0.0`, every the CMS is loaded you will see the latest minor/patch versions, ensure you have the most advanced and reliable version.

> [!NOTE]
>
> Until the point of writing this TIL, the latest major version of Decap CMS is **3**.

## Installation

Create a folder called `/admin` and placed in either 1 of 2 places:
- SSG framework's output directory. (e.g. `/_site` for 11ty, `/public` for NextJS)
- Root directory. Config the front-end framework to add `/admin` into the output directory during build.

```js
// eleventy.config.mjs
// ...
eleventyConfig.addPassthroughCopy("admin");
```

Inside `/admin`, there are 2 files: `index.html` and `config.yml`

1. `admin/config.yml`, the heart of Decap CMS.
1. `admin/index.html`, the entry point of Decap CMS admin interface. 

It's a basic HTML file that loads the Decap CMS JS file. Users will navigate to `https://input-your-site-here.com/admin` to access it.

```html
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <meta name="robots" content="noindex" />
    <title>Content Manager</title>

    <!-- Note the "type" and "rel" attribute values, which are required. -->
    <!-- <link href="custom/path/to/config.yml" type="text/yaml" rel="cms-config-url"> -->
  </head>

  <body>
    <script>
    function loadFallbackScript() {
      console.error("Failed to fetch jsDelivr. Fetching from unpkg...");
      const unpkgScript = document.createElement('script');
      unpkgScript.src = "https://unpkg.com/decap-cms@^3.0.0/dist/decap-cms.js";
      unpkgScript.onerror = () => {
        console.error("Failed to fetch Decap CMS from both jsDelivr and unpkg!");
        // Optionally notify the user or try a local fallback
      };
      document.body.appendChild(unpkgScript);
    }
    </script>
    <script src="https://cdn.jsdelivr.net/npm/decap-cms@3/dist/decap-cms.js" onerror="loadFallbackScript()"></script>

    <!-- custom id widget -->
    <!-- cre: https://github.com/decaporg/decap-cms/issues/1407#issuecomment-456714505 -->
    <script>
      CMS.registerWidget(
        'nanoid',
        createClass({
          getDefaultProps: function () {
            return {
              value: ''
            }
          },
          nanoid: (e = 21) => {
            const a = "useandom-26T198340PX75pxJACKVERYMINDBUSHWOLF_GQZbfghjklqvwyzrict";
            let t = "", r = crypto.getRandomValues(new Uint8Array(e));
            for (let n = 0; n < e; n++)
              t += a[63 & r[n]];
            return t;
          },
          componentDidMount: function () {
            const value = this.props.value;
            const onChange = this.props.onChange;
            const nanoid = this.nanoid;

            if (!value) {
              onChange(nanoid());
            }
          },
          render: function () {
            const value = this.props.value;
            const classNameWrapper = this.props.classNameWrapper;
            const forID = this.props.forID;

            return h('span', {
              id: forID, className: classNameWrapper, style: {
                opacity: 0.7
              }
            }, value);
          }
        })
      );
    </script>
  </body>
</html>
```

## Choose backend

- Netlify and Netlify Identity: https://decapcms.org/docs/choosing-a-backend/
- Cloudflare Pages: https://github.com/i40west/netlify-cms-cloudflare-pages

## [Decap CMS Configuration File Cheatsheet](https://decapcms.org/docs/configuration-options/)

**NOTE:** from now on, content file (or "Page", "Markdown file with frontmatter") is referred to as "Entry"


```yml
# when using the default proxy server port
local_backend: true

# default, all entries created/modified are committed DIRECTLY into main branch
# have more control 
publish_mode: editorial_workflow # def="simple"

# specify backend protocol
backend:
  name: git-gateway   # for GitHub + GitLab repo
  branch: main        # default=master

  # supported template tags:
  # {{slug}}: the url-safe filename of the entry that changed
  # {{collection}}: the value of the `label` or `label_singular` of the collection containing the entry that changed (it's the entry, not collection, that changed)
  # {{path}}: the full path to the file changed
  # {{message}} : the relevant message based on the current change (e.g. the `create` message when an entry is created)
  # {{author-login}}: username of the account who made the change
  # {{author-name}}: name in the user profile of the account who made the change, can be empty string if user doesn't set it

  commit_messages:
    create: "Create {{collection}} “{{slug}}” by {{author-name}}"
    update: "Update {{collection}} “{{slug}}” by {{author-name}}"
    delete: "Delete {{collection}} “{{slug}}” by {{author-name}}"
    uploadMedia: "Upload “{{path}}” by {{author-name}}"
    deleteMedia: "Delete “{{path}}” by {{author-name}}"
    openAuthoring: "{{message}} by {{author-name}}"

# DecapCMS allow upload medias directly within editor, media from ALL collections
# are saved under ONE directory
# Typically, it's where your SSG expecting static files
# NOTE: this setting is relative to the project root
media_folder: "_site/images/uploads"

# specify where the media files uploaded will be found in the published site
# e.g. an image `john-wick.png` being uploaded by an image widget "avatar"
# - the file will be saved at "_site/images/uploads/john-wick.png"
# - the `avatar:` field for the entry, set to "/images/uploads/john-wick.png"
# NOTE: if blank, inferred from `media_folder` with a starting slash `/` if not specified
public_folder: "/images/uploads"

# media_library:                    # connect to 3rd-party media gallary
site_url: https://iamhung.top       # provide a URL to your published site
# display_url:                      # include the link in the fixed area at the top of the CMS UI
                                    # def=site_url's value
# logo_url:                         # change the logo displayed at the top of the login page
# locale:                           # def=en, change to "vi". NOTE: Decap CMS also supports "vi"
# show_preview_links:               # def=true, display URL to preview upcoming change
# search:                           # def=true. load all collections' entries on remote repositories
                                    # Might trigger rate limits, best to set to false
slug:
  encoding: "ascii"             # only allows alphanumeric, underscore, hyphen and tilde
                                # "unicode" (default), allows non-ASCII to exist in URL.
  clean_accents: true           # remove diacritics from slug characters before sanitizing
  #sanitize_replacement: "_"    # def="-". It's used to substiture unsafe characters.

editor:
  preview: false # disable the preview pane for ALL collections

collections:
  # Folder Collection Example
  - name: "blog"            # collection's unique identifier, used in URL routes, 
                            # e.g. /admin/collections/blog
    label: "blog"           # displayed in Decap CMS UI
    folder: "_posts/blog"   # path to the folder where the Entries are stored
    create: true            # allow users creating new Entry in collection
    slug: "{{year}}-{{month}}-{{day}}-{{slug}}"   # filename template
    # {{slug}} is the URL-safe version of the Entry's `title` field
    fields:                 # the fields for each Entry, in frontmatter
      - { label: "Layout", name: "layout", widget: "hidden", default: "blog" }
      - { label: "Title", name: "title", widget: "string" } # NOTE: slugify target 
      - { label: "Publish Date", name: "date", widget: "datetime" }
      - { label: "Featured Image", name: "thumbnail", widget: "image" }
      - { label: "Rating (scale of 1-5)", name: "rating", widget: "number" }
      - { label: "Body", name: "body", widget: "markdown" }
  
  # Filter example
  - name: "posts"
    label: "Posts"
    folder: "_posts"
    filter:
      field: language
      value: en
    fields:
      - { label: "Language", name: "language" }

  # Nested Collections
  - label: "Nested Pages"
    name: "nested"
    label_singular: "Page"
    folder: "content/pages" # NOTE: must be Folder collection
    create: true
    fields:
      - { label: "Title", name: "title", widget: "string" }
      - { label: "Body", name: "body", widget: "markdown" }
    nested:
      depth: 3                # max depth to show
      summary: "{{title}}"    # optional summary for a tree node, defaults to the inferred title field
    # `meta` obj with `path` property allows editing the path of entries
    # change `path` property = move an entire sub tree of the entry to the new location
    meta: { path: { widget: string, label: "Path", index_file: "index" } }

  # File Collection Example
  - label: "Pages"
    name: "pages"
    # NOTE: `files:` and `folder:` are mutual exclusive.
    # NOTE: unique files inside File collection must be existed already and contains valid value
    # (e.g. `.json` file must contain empty object `{}`)
    files:  # A list that contains one or more uniquely files
      - label: "About Page"
        name: "about"
        file: "src/content/about.yml"
        fields:
          - {label: Title, name: title, widget: string}
          - {label: Intro, name: intro, widget: markdown}
          - label: Team
            name: team
            widget: list
            fields:
              - {label: Name, name: name, widget: string}
              - {label: Position, name: position, widget: string}
              - {label: Photo, name: photo, widget: image}

      - label: "Locations Page"
        name: "locations"
        file: "src/content/locations.yml"
        fields:
          - {label: Title, name: title, widget: string}
          - {label: Intro, name: intro, widget: markdown}
          - label: Locations
            name: locations
            widget: list
            fields:
              - {label: Name, name: name, widget: string}
              - {label: Address, name: address, widget: string}

  # Complex Folder Collection
  - name: "blog"
    label: "Blogs"
    label_singular: "Blog"      # def=label's value
    identifier_field: "key"     # def="title"
                                # "title" value is used as the unique identifier for the entry, entry's title when viewing a list of entries and slug creation
    description: "A list of blog posts"
    folder: "src/posts"         # create entry src/posts/slug-field-value.md
    path: "{{year}}/{{slug}}"   # create entry src/posts/2025/slug-field-value.md
                                # if `path:` specified, media_folder set to "", entry and media lives together
    media_folder: "{{media_folder}}/work"     # per-collection uploaded media save location
    public_folder: "{{public_folder}}/work"   # per-collection uploaded media referenced on published site
    # template tags supported:
    # - {{dirname}} - the path to the file's parent directory, relative to the collection's `folder` field
    # - {{filename}} 
    # - {{extension}}
    # - {{media_folder}} - the global media_folder
    # - {{public_folder}} - the global public_folder

    filter:                   # Per-collection filter, different from Relation widget filter
      field: "foo"
      value: "bar"
    create: true              # NOTE: Folder Collection only
    publish: false            # hide the UI for publishing
    hide: true                # hide the collection in CMS UI
    delete: false             # def=true, allow users from deleting in a collection
    extension: md             # Determine how collection files are parsed and saved. 
                              # NOTE: "Markdown file with YAML-formatted frontmatter" offer
                              # the best balance of readability, flexibility, compatibility.
    format: "frontmatter"     # Determine how collection files are parsed and saved. 
                              # This field is inferred based on `extension` field.
                              # e.g. `extension: md` so `format:` will take `frontmatter` value, which is only processed the data formatter and leave the body.
    # change the frontmatter delimiter
      # optional, def="---"
    frontmatter_delimiter: "~~~"

    # template for entry's filename
    # def="{{slug}}"
    # supported template tags:
      # {{title}}, {{foo}}, etc. - entry's fields
      # {{slug}} - url-safe version of the value of entry's `title:` (or `identified_field:` ) field
      # {{fields.slug}} - entry's `slug:` field.
      # {{year}}, {{month}}, {{day}}, {{hour}}, {{minute}}, {{second}} - extracted from entry's `date` field, or entry's creation date on OS filesystem metadata.
    slug: "{{year}}-{{month}}-{{day}}-{{slug}}"

    # preview the rendered version of the entry on live site
      # optional. def="/" (site root)
      # supported template tags:
        # {{slug}} - same as above
        # {{year}}, {{month}}, {{day}} - same as above
        # {{dirname}} - path to entry's parent directory
        # {{filename}} - extension-less filename
        # {{extension}} - file extension only
    preview_path: "people/{{slug}}" 
    # preview_path: "blog/{{year}}/{{month}}/{{slug}}"

    # sometimes, you don't want to use entry's `date:` field or entry's OS filesystem metadata for date-based template tags extraction.
      # optional
    preview_path_date_field: "updated_on" 
                                                       
    # customize the collection's list view
    # docs: https://decapcms.org/docs/summary-strings/
      # optional
      # supported template tags:
        # {{foo}}, {{bar}}, {{baz}}, etc. any fields that `slug:` can access
        # {{dirname}}
        # {{filename}}
        # {{extension}}
        # {{commit_date}}
        # {{commit_author}}
      # transformation, using Nunjucks' filter syntax:
        # upper
        # lower
        # date("INSERT_FORMAT_STRING")
        # default("INSERT_DEFAULT_STRING")
        # ternary("INSERT_STRING_FOR_TRUE", "INSERT_STRING_FOR_FALSE")
          # TODO: Find out the behavior for non-boolean field? What is the implicit type coercion behavior?
        # truncate(INSERT_NUMBER) or truncate(INSERT_NUMBER, "INSERT_STRING")
          # docs: https://mozilla.github.io/nunjucks/templating.html#truncate
    summary: "{{title | upper}} - {{date | date('YYYY-MM-DD')}} – {{body | truncate(20, '...')}}"        

    # list of sort fields to show in the CMS UI
      # optional
    sortable_fields: ['commit_date', 'title', 'commit_author', 'language.en'] 

    # a list of predefined view filters to show in the Decap CMS UI
      # optional, def=empty list
    view_filters:
      - label: "Alice's and Bob's Posts"
        field: author
        pattern: 'Alice|Bob'
      - label: 'Posts published in 2020'
        field: date
        pattern: '2020'
      - label: Drafts
        field: draft
        pattern: true

    view_groups:
      - label: Year
        field: date
        pattern: \d{4}
      - label: Drafts
        field: draft
      # optional, def=empty list
      # a list of predefined view groups to show in the Decap CMS UI

    editor:
      preview: false
      # optional, def=true
      # disable the preview pane for the collection or file

    fields:
      # String widget
      # Multi-line syntax
      - name: "blog"  # maps editor UI widgets to field-value pairs in the saved file
        label: "Blog"
          # required, field label in the editor UI.
        widget: "string"
          # required, inputs for Decap CMS editor interface
          # by core, it's a React component that receives user input and outputs a serialized value
          # there are commonly used widget: "boolean", "datetime", "file", "hidden", "list", "image", "number", "object", "relation", "select", "string", "text"
        default: "A quick brown fox jumps over the lazy dog"
          # optional
          # can be specified dynamically using URL query parameters
          # however, you will need to write JS code to populate this URL query parameters somehow
        hint: "Please input your full name here."
        required: false
          # optional
          # by default, every fields are required
        pattern: [".{20,}", "Must have at least 20 characters"] 
          # optional
          # add field validation rule using regex
        comment: "This is a multiline\ncomment"  
          # optional
          # only supported in `extension: yaml`

      # Recommended: One-liner syntax is much cleaner
      # However, it's not recommended for field whose widget contains nested structure (e.g. "object", "list", "image", ...)
      - { label: "Layout", name: "layout", widget: "hidden", default: "blog" }
        # Q: What about the "layout" field? That's not supposed to be supplied by non-tech user
        # A: Hide it, and give it a default value. 
        # CAUTION: Some fields are best to be handled by the front-end framework.

      # Relation widget
      - label: "Team"
        name: "team"
        widget: "relation"
        collection: "people"      # Name of the "referenced" collection
        value_field: "key"        # Name of the field from the "referenced" collection's entry, whose value
                                  # will be stored inside the "referencing" collection's entry (i.e. "Team")
                                  # e.g. a foreign key inside a table which is the id column of another table

        search_fields: ["name"]   # List of the "referenced" collection's entry's fields 
                                  # that will be used as search criteria
                                  # NOTE: avoid set value_field to nanoid key
                                  # e.g. the UI will search the "people" collection's entry by "name" field.

        display_fields: ["name"]  # List of the "referenced" collection's entry's fields
                                  # that will be rendered in the autocomplete menu of the control.
                                  # After searching, the generated UI input display each person's name
                                  # Of course, beside name, you can display other fields that might serve as criteria choosing decision)
        default: "foo bar"
        multiple: true
        min: 1
        max: 50
        options_length: 30        # def=20, limit the number of options presented to user
                                  # it should be less than `max: `
        filters:                  
          # a list of pairs of `field` and `values`, 
          # which are the name of field and a list of 1 or more allowed values
          # a collection item satisfies a filter if the value of `field` is one of the values in `values`
          - field: draft
            values: [false]
          - field: title
            values: ['post about cats', 'post about dogs']

      - label: "Puppy Count"
        name: "puppies"
        widget: "number"
        default: 2
        value_type: "int" # a list of pairs of `field` and `values`, 
        min: 1
        max: 101
        step: 2

      # Object widget
      - label: "Featured Work"
        name: "featuredWork"
        widget: "object"
        summary: "{{title}}: {{ summary | truncate(20, '...')}}" # display when the obj is collapsed
        collapsed: true   # def=false. By default, disable collapsing the widget
        fields:
          - { label: "Title", name: "title", widget: "string" }
          - { label: "Summary", name: "summary", widget: "string" }
      
      # Datetime widget
      - label: "Publish Date"
        name: "date"
        widget: "datetime"
        default: "{{now}}"
        format: "YYYY-MM-DD"
        time_format: false
        # CAUTION: extremly buggy and not reliable.
        # CAUTION: Can't change date picker UI from inside Decap CMS
        # CAUTION: Mix and match ISO format date with custom format date make sorting behavior wrong.
      
      # List widget
      - label: "Tags"
        name: "tags"
        widget: "list"
        #field: { label: "Value", name: "value", widget: "string" }
        fields: # optional
          - { label: "Source", name: "src", widget: "string" }
          - { label: "Alt Text", name: "alt", widget: "string" }
          # without `fields:`, the list widget defaults to a text input for entering comma-separated values
          # with `fields:`, the list widget contains a repeatable child widget, with controls for adding, deleting, and re-ordering the repeated widgets.
        default:
          - { src: "/img/tennis.jpg", alt: "Tennis" }
          - { src: "/img/footbar.jpg", alt: "Football" }
          # without `fields`, it's a list of strings (e.g. ["foo", "bar"])
          # with `fields`, it's an array of list items
        allow_add: false # by def=true, don't hide the button to add additional items
        collapsed: false # by def=true, collapse the widget
        minimize_collapsed: true  # by def=false, prevent hiding all of its entries and show summaries
        label_singular: "Tag"
          # optional
          # override the text showing on the add button
          # NOTE: meaningless if you're not using `fields` to tweak its UI
        min: 2
        max: 10
        add_to_top: true
          # optional, def=false
          # new entries will be added to the top of the list
          # NOTE: meaningless if you're not using `fields` to tweak its UI
```

### 4. Access your content

Content fetched in the admin UI matches the content in the hosted repository, which might be different from the locally running site.

Content saved using UI saves directly to the hosted repository, even if you're running the admin UI locally.

## Customization

### Manual Initialization

For projects with bigger scope, you can create custom widgets and set up dynamic default values and replace SSOT `config.yml` with a JS file for better scalability and maintainability, [as recommended by Mr. Kaluzny](https://mrkaluzny.com/blog/dry-decap-cms-config-with-manual-initialization).

Custom widgets can be created, set up dynamic default values and replace `config.yml` - the SSOT - with JavaScript file with Manual Initialization for better scalability and maintainability, 

Manual Initialization can be done via two methods: 
- `import` from `npm` package
- `<script>` tag inside `admin/index.html`

### Custom widget

Decap CMS is "barely" production-ready. There are a lot of widgets that wasn't officially supported so engineers have to rely on 3rd-party widgets.

I personally prefer zero dependencies for my data sources to maximize security. I've reviewed their code and rewritten it so that it can fit inside a single `<script>` tag.

```html
<!-- custom id widget -->
<!-- cre: https://github.com/decaporg/decap-cms/issues/1407#issuecomment-456714505 -->
<script>
  // CMS.registerWidget(name, control, [preview], [schema]);
  CMS.registerWidget(
    // two benefits of using nanoid
    // one, Decap CMS doesn't support auto increment
    // two, non-tech user doesn't need to remember the last ID
    "nanoid", // string, accessed via `widget:` field in `config.yml`
    createClass({
      getDefaultProps: function () {
        return {
          value: "",
        };
      },
      nanoid: function (options) {
        const options = options || {};
        const size = options.size || 21;
        const url =
          options.url ||
          // "Uint8ArdomValuesObj012345679BCDEFGHIJKLMNPQRSTWXYZ_cfghkpqvwxyz-";
          "useandom-26T198340PX75pxJACKVERYMINDBUSHWOLF_GQZbfghjklqvwyzrict";
        let id = "";

        if (typeof self === "undefined" || (!self.crypto && !self.msCrypto)) {
          while (0 < size--) {
            id += url[(Math.random() * 64) | 0];
          }
          return id;
        }

        // else
        const crypto = self.crypto || self.msCrypto;
        const bytes = crypto.getRandomValues(new Uint8Array(size));
        while (0 < size--) {
          id += url[bytes[size] & 63];
        }
        return id;
      },
      componentDidMount: function () {
        const value = this.props.value; // current field value
        const onChange = this.props.onChange; // callback function to update the field value
        const nanoid = this.nanoid;

        // if field is empty, initialize it with a nanoid
        if (!value) {
          onChange(this.nanoid());
        }
      },
      render: function () {
        const value = this.props.value;
        const classNameWrapper = this.props.classNameWrapper; // class name to apply CMS styling to the field
        const forID = this.props.forID; // unique identifier for the field

        // h is alias for React.createElement
        return h(
          "span",
          {
            id: forID,
            className: classNameWrapper,
          },
          value
        );
      },
    })
  );
</script>
```

## References

1. [Decap CMS Official Documentation](https://decapcms.org)
