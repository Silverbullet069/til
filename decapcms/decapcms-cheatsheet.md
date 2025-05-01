# DecapCMS Cheatsheet

<!-- tl;dr starts -->

Decap CMS is my go-to CMS solution for building personal web projects, as mentioned in [My Ultimate Web Tech Stack](../0-misc/my-ultimate-web-tech-stack.md).

<!-- tl;dr ends -->

## Why I choose Decap CMS?

It is a Git-based, open-source CMS.

- Its content, alongside the code is stored inside GitHub. This enables content versioning, content updates handling directly in Git and mult-channel publishing (major providers such as Cloudflare, AWS, ...)
- GitHub Actions - the CI/CD tool that's highly integrated with GitHub, can use content hosted on GitHub for remote build process.
- It is framework-agnostic. It can be used with any static site generator.
- It provides a web-based admin panel UI with robust editor and can be hosted on cloudf providers (either by Netlify which is supported officially or Cloudflare Developer Platform, my currently chosen vendor)

## What is it actually?

At its core, Decap CMS is an open-source React application, that acts as a wrapper for the Git workflow, using GitHub, GitLab and Bitbucket API.

Hooking Decap CMS to your website is basically adding a tool for content editors to make commits to the GitHub repository without touching code or learning Git and running Git CLI.

_Pros:_

1. **Fast, web-based UI:** non-tech users can access the CMS on browser. It has rich-text editing, real-time preview, drag-and-drop media uploads.
2. **Easy installation:** you can drop-in a few files to the project root - admin panel UI and serverless functions - alongside your existing codebase.
3. **Modern authentication:** using GitHub, GitLab or Bitbucket JWT.
4. **Flexible content types:** support unlimited number of content types with custom fields.
5. **Fully extensible:** custom-styled previews, UI widgets, editor plugins.

## Releases

There are 2 ways to update Decap CMS:

1. Package Manager: `npm` and `yarn`.
2. CDN: you can use and update your CMS through CDN like Unpkg by going into `admin/index.html` and update the `<script src="https://unpkg.com/decap-cms@^3.0.0/dist/decap-cms.js">`. It's recommended that you use `^3.0.0`, the CMS does all updates except major versions automatically, this ensures you always have the most advanced and reliable version
   > Latest version until the time of writing this page is `3.6.2`.

## FOUR step of adding Decap CMS to your existing site

### 1. Install Decap CMS

You can install Decap CMS via 2 methods, I chose the CDN method.

Create a folder called `/admin`. This folder consists of Decap CMS files that are sotred at the root of the published site.

`/admin` can be placed in 2 places:

- Inside static file generator's output directory. (e.g. for 11ty, it's `/_site`)
- Root directory, but config the framework so `/admin` is copied into the output directory during build process (e.g. for 11ty, add this line into `eleventy.config.mjs`: `eleventyConfig.addPassthroughCopy("admin");`)

Inside `/admin`, there are 2 files: `index.html` and `config.yml`

- `admin/index.html` is the entry point for Decap CMS admin interface, it's a basic HTML file that loads the Decap CMS JS file. Users will navigate to `https://input-your-site-here.com/admin` to access it.

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
    <!-- Include the script that builds the page and powers Decap CMS -->
    <script src="https://unpkg.com/decap-cms@^3.0.0/dist/decap-cms.js"></script>

    <!-- Should Unpkg be any issue, jsDelivr can be used as an alternative source -->
    <!-- <script src="https://cdn.jsdelivr.net/npm/decap-cms@^3.0.0/dist/decap-cms.js"></script> -->
  </body>
</html>
```

- `admin/config.yml` is the heart of DecapCMS installation.

### 2. Choose backend for Decap CMS

Official documentation recommendeds using Netlify and Netlify Identity, but after reading [a blog post by Cassey Lottman about adding Decap CMS to 11ty](https://cassey.dev/11ty-on-cloudflare-pages/#decap-cms), I've found a way to [host the Decap CMS web-based UI on Cloudflare Pages](https://github.com/i40west/netlify-cms-cloudflare-pages).

### 3. Configure Decap CMS

There are a few options you should know.

```yml
# when using the default proxy server port
local_backend: true
publish_mode: editorial_workflow # does not support in `local_fs` backend so it will switch to `simple` automatically

backend:
  name: git-gateway # specify backend protocol, Git Gateway is an open-source API that acts as a proxy between authenticated users of your site and the repository
  # branch: main        # optional, def=master

  commit_messages:
    create: "Create {{collection}} “{{slug}}” by {{author-name}}"
    update: "Update {{collection}} “{{slug}}” by {{author-name}}"
    delete: "Delete {{collection}} “{{slug}}” by {{author-name}}"
    uploadMedia: "Upload “{{path}}” by {{author-name}}"
    deleteMedia: "Delete “{{path}}” by {{author-name}}"
    openAuthoring: "{{message}} by {{author-name}}"

    # supported template tags:
    # {{slug}}: the url-safe filename of the entry that changed
    # {{collection}}: the value of the `label` or `label_singular` of the collection containing the entry that changed (it's the entry, not collection, that changed)
    # {{path}}: the full path to the file changed
    # {{message}} : the relevant message based on the current change (e.g. the `create` message when an entry is created)
    # {{author-login}}: username of the account who made the change
    # {{author-name}}: name in the user profile of the account who made the change, can be empty string if user doesn't set it

# specify where to save uploaded files, it's relative to the project root
media_folder: "src/images"

# indicates where the media files are found in the published site
# <img> tag `src` attribute use this field, that's why we usually start the path at the site root, using the opening slash `/`
# if not specified, inferred from `media_folder:`
public_folder: "/images"

# media_library:  # optional, connect to 3rd-party media gallary
# site_url:       # optional, provide a URL to your published site
# display_url:    # optional, include the link in the fixed area at the top of the CMS UI
# logo_url:       # optional, CMS UI change the logo displayed at the top of the login page
# locale:         # def=en. Decap CMS also supports `vi`, which is very good for Dad
# show_preview_links:  # def=true
# search:         # def=true. Might trigger rate limits, consider disabling it.
slug:
  encoding: "ascii" # def="unicode". "ascii" only allows alphanumeric, underscore, hyphen and tilde
  clean_accents: true # remove diacritics from slug characters before sanitizing
  #sanitize_replacement: "_"  # def="-". It's used to substiture unsafe characters.

#editor:
###preview: false # disable the preview pane for ALL collections

# NOTE: from now on, each content file (or "Markdown file with frontmatter") is referred to as "entry"

# prettier-ignore
collections:
  - label: "Nested Pages"
    name: "nested"
    label_singular: "Page"
    folder: "content/pages"
      # must be Folder collection
    create: true
    fields:
      - { label: "Title", name: "title", widget: "string" }
      - { label: "Body", name: "body", widget: "markdown" }
    nested:
      depth: 3 # max depth to show
      summary: "{{title}}"
      # show to collection folder structure
    meta: { path: { widget: string, label: "Path", index_file: "index" } }
      # add a meta obj with path property allows editing the path of entries
      # moving an existing entry will move the entire sub tree of the entry to the new location

  - label: "Pages"
    name: "pages"
    files:
      # File collection
      # A list that contains one or more uniquely files
      
      # NOTE: there can only be one field among two fields `files:` and `folder:` in one collection
      # NOTE #2: files listed in a File collection must already exist in the hosted repository and contains valid value (e.g. `.json` file must contain empty object `{}`)

      - label: "About Page"
        name: "about"
        file: "site/content/about.yml"
        fields:
          - {label: Title, name: title, widget: string}
          - {label: Intro, name: intro, widget: markdown}
          - label: Team
            name: team
            widget: list
            #field:
            fields:
              - {label: Name, name: name, widget: string}
              - {label: Position, name: position, widget: string}
              - {label: Photo, name: photo, widget: image}

      - label: "Locations Page"
        name: "locations"
        file: "site/content/locations.yml"
        fields:
          - {label: Title, name: title, widget: string}
          - {label: Intro, name: intro, widget: markdown}
          - label: Locations
            name: locations
            widget: list
            #field:
            fields:
              - {label: Name, name: name, widget: string}
              - {label: Address, name: address, widget: string}

  - label: "Blog" 
      # optional, def=`name:` field's value
      # what will be displayed in the editor of CMS UI
    label_singular: "Blog" 
      # optional, def=`label:` field's value
      # what will be displayed in the editor of CMS UI
    name: "blog" 
      # required
    identifier_field: "key" 
      # def="title"
      # its value, is the name of the field, whose value, will be used as the unique identifier for the entry.
      # this unique identifier will be used in slug creation.
    description: "A list of blog posts"
    folder: "src/posts"
      # required
      # Folder collection - one or more files with the same format, fields, configurations options, best for blog posts, products, ...
      # NOTE: if this `folder:` field is used, you can't use `files:` field
    # ======================================================================== #
    path: "{{year}}/{{slug}}"
      # optional
      # by default, CMS stores Folder collection's entry under the `folder:` field, e.g. "src/posts/post-title.md"
      # however, if you want to create nested folders, like "src/posts/2025/post-title.md", specify `path:` field like above
      # NOTE: if `path` is specified on a `folder` collection, `media_folder` defaults to ""
      # NOTE: if so, entry and media must live together
    media_folder: "{{media_folder}}/work" 
    public_folder: "{{public_folder}}/work" 
      # optional
      # per-collection, override global setting
      # if empty string => put media in the same directory as the entry, where the media is served as well
      # template tags supported:
        # {{dirname}} - the path to the file's parent directory, relative to the collection's `folder` field
        # {{filename}} 
        # {{extension}}
        # {{media_folder}} - the global media_folder
        # {{public_folder}} - the global public_folder
    # ======================================================================== #
    filter: {field: "foo", value: "bar"}
      # Optional. 
      # Can only be used if it's Folder collections
    create: true 
      # allow users to create new items in the collection
    publish: false
      # def=true.
      # Ignore if `publish_mode: editorial_workflow` not existed. Hide UI publishing controls for a collection,
    hide: true
      # def=false.
      # Hide the collection in CMS UI. Useful when using the relation wedget to hide referenced collections.
      # to hide fields, use `widget: hidden`
    delete: false  
      # def=true
      # Prevent users from deleting in a collection
    extension: md 
      # Optional.
      # Determine how collection files are parsed and saved. 
      # NOTE: IMO, "Markdown file with YAML-formatted frontmatter" offer the best balance of readability, flexibility, compatibility.
    format: "frontmatter"
      # Optional.
      # Determine how collection files are parsed and saved. This field is inferred based on `extension` field.
      # NOTE: `extension: md` so `format:` will take `frontmatter` value.
    frontmatter_delimiter: "~~~"
      # Optional. 
      # NOTE: IMO, triple hyphens is good enough.
    slug: "{{year}}-{{month}}-{{day}}-{{slug}}"
      # template for filename for the entry
      # template tags supported:
        # {{title}}, {{foo}}, ...: any field that's existed inside the content file
        # {{slug}}: a url-safe version of the `title` field (or `identified_field`'s value)
        # {{fields.slug}}: if your content file happens to contain a slug field.
        # {{year}}, {{month}}, {{day}}, {{hour}}, {{minute}}, {{second}}: extracted from `date` field, or file's creation date on OS.
    preview_path: "people/{{slug}}" # test
    #preview_path: "blog/{{year}}/{{month}}/{{slug}}"
      # optional
      # a string representing the path where content in this collection can be found on the live site. If not specified, it will lead to the site root.
      # template tags supported:
        # {{slug}} - the value from above `slug`, not just the url-safe identifier
        # {{year}}, {{month}}, {{day}} - date-based template tags. If preview_path_date_field not specified, they're pulled from `date` field.
        # {{dirname}} - the path to the file's parent directory
        # {{filename}} - the filename without extension part
        # {{extension}} - the file extension
    preview_path_date_field: "updated_on"
      # optional
      # if not provided, `preview_path` will check for `date` field.
      # specified if you want another field ( to be used
    fields:
      # required
      # maps editor UI widgets to field-value pairs in the saved file
      - name: "blog"
          # required, field name in the entry's front matter.
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
      - { label: "Layout", name: "layout", widget: "hidden", default: "blog" }
        # Q: What about the "layout" field? That's not supposed to be supplied by non-tech user
        # A: Hide it, and give it a default value. 
        # CAUTION: You don't have to write EVERY FIELDS inside `config.yml`. Sometimes, it's better to NOT include developer-responsible fields then using "widget: hidden" to hide them from non-tech workers.

        # NOTE: It's recommended to use one-liner syntax, much more clean
        # NOTE: Not recommende for field whose widget contains nested structure (e.g. "object", "list", "image", ...)
      - label: "Team"
        name: "team"
        widget: "relation"
        collection: "people"
          # name of the referenced collection
        value_field: "key"
          # name of the field from the referenced collection, whose value will be stored inside the referencing collection for the relation
        search_fields: ["name"]
          # list of 1 or more names of fields in the referenced collection to search for.
          # e.g. the generated UI input will search the "people" collection by "name" field
          # if value_field is some key of nanoid key, we wouldn't want to search for nanoid right?
        display_fields: ["name"]
          # List of 1 or more names of fields in the referenced collection that will render in the autocomplete menu of the control.
          # After searching, the generated UI input display each person's name (of course you can display more fields serve as criteria for your choosing decision)
          # On selection, the author's name is saved for the field "team"
        #default: "foo bar"
        multiple: true
        #min: 1
          # minimum number of items
        #max: 50
          # maximum number of items
        #options_length: 30
          # def=20
          # limit the number of options presented to user
          # it should be less than `max: `
        #filters: 
          # - field: draft
          #   values: [false]
          # - field: title
          #   values: ['post about cats', 'post about dogs']
          
          # a list of pairs of `field` and `values`, which are the name of field and a list of 1 or more allowed values
          # a collection item satisfies a filter if the value of `field` is one of the values in `values`

      - label: "Puppy Count"
        name: "puppies"
        widget: "number"
        default: 2
        value_type: "int"
          # optional, but if isn't specified, the value is stored as string
        min: 1
        max: 101
        step: 2

      - label: "Featured Work"
        name: "featuredWork"
        widget: "object"
        summary: "{{title}}: {{summary | truncate(20, '...')}}"
          # displayed when the obj is collapsed
        collapsed: false
          # optional, def=true
          # prevent collapsing the widget inside `fields:` right after UI loading (not the parent widget)
        fields:
          - { label: "Title", name: "title", widget: "string" }
          - { label: "Summary", name: "summary", widget: "string" }
      
      - label: "Publish Date"
        name: "date"
        widget: "datetime"
        default: "{{now}}"
        format: "YYYY-MM-DD"
        time_format: false
          # NOTE: extremly buggy and not reliable. But mmong the Git-based, open-source CMS, Decap CMS is the best :v
          # Can't change date picker UI from inside Decap CMS
          # Mix and match ISO format date with custom format date will render the sorting behavior wrong.
      
      - label: "Tags"
        name: "tags"
        widget: "list"
        fields:
          - { label: "Source", name: "src", widget: "string" }
          - { label: "Alt Text", name: "alt", widget: "string" }
          # without this `fields:`, the list widget defaults to a text input for entering "comma-separated values"
          # with `fields:`, the list widget contains a repeatable child widget, with controls for adding, deleting, and re-ordering the repeated widgets.
        default:
          - { src: "/img/tennis.jpg", alt: "Tennis" }
          - { src: "/img/footbar.jpg", alt: "Football" }
          # without `fields`, it can be a list of strings (e.g. ["foo", "bar"])
          # with `fields`, it can be an array of list items (e.g above)
        allow_add: false
          # optional, def=true
          # hide the button to add additional items, or prevent addition
          # NOTE: meaningless if you're not using `fields` to tweak its UI
        collapsed: false
          # optional, def=true
          # prevent collapsing the widget inside `fields:` right after UI loading (not the parent widget)
          # NOTE: meaningless if you're not using `fields` to tweak its UI
        minimize_collapsed: true
          # optional, def=false
          # hide all of its entries, instead of showing summaries
          # NOTE: meaningless if you're not using `fields` to tweak its UI
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

    summary: "{{title | upper}} - {{date | date('YYYY-MM-DD')}} – {{body | truncate(20, '...')}}"
      # optional
      # allow the customization of the collection list view
      # supported any field that `slug:` field can access: 
        # {{foo}}, {{bar}}, {{baz}}, ... 
        # {{dirname}}
        # {{filename}}
        # {{extension}}
        # {{commit_date}}
        # {{commit_author}}.
      # can be applied transformation, using filter notation syntax
        # upper
        # lower
        # date("INSERT_FORMAT_STRING")
        # default("INSERT_DEFAULT_STRING")
        # ternary("INSERT_STRING_FOR_TRUE", "INSERT_STRING_FOR_FALSE")
          # TODO: What is the behavior for non-boolean field? What is the implicit type coercion behavior?
        # truncate(INSERT_NUMBER) or truncate(INSERT_NUMBER, "INSERT_STRING")
          # read more: https://mozilla.github.io/nunjucks/templating.html#truncate

    sortable_fields: ['commit_date', 'title', 'commit_author', 'language.en']
      # optional
      # list of sort fields to show in the CMS UI

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
      # optional, def=empty list
      # a list of predefined view filters to show in the Decap CMS UI

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
```

### 4. Access your content

Content fetched in the admin UI matches the content in the hosted repository, which might be different from the locally running site.

Content saved using UI saves directly to the hosted repository, even if you're running the admin UI locally.

## Customization

### Manual Initialization

Official documentation shows that you can create custom widgets, set up dynamic default values and replace `config.yml` - the SSOT - with JavaScript file with Manual Initialization for better scalability and maintainability, [as recommended by Mr. Kaluzny](https://mrkaluzny.com/blog/dry-decap-cms-config-with-manual-initialization). Manual Initialization can be done via two methods: `import` from `npm` package or `<script>` tag. It doesn't limit to developers that installed via `npm` (my grave mistake back then).

For simple use cases + zero dependencies, I suggest you stay with `config.yml`.

### Custom widget

Decap CMS is "barely" production-ready. There are a lot of widgets that wasn't officially supported so engineers have to rely on 3rd-party widgets.

I personally prefer zero dependencies for my data sources to maximize security. I've reviewed their code and rewritten it so that it can fit inside a single `<script>` tag.

```html
<!-- custom id widget -->
<!-- cre: https://github.com/decaporg/decap-cms/issues/1407#issuecomment-456714505 -->
<script>
  // CMS.registerWidget(name, control, [preview], [schema]);
  CMS.registerWidget(
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
