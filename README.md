# Wagtail F Richtext

[![test](https://github.com/nickmoreton/wagtail-f-richtext/actions/workflows/test.yml/badge.svg)](https://github.com/nickmoreton/wagtail-f-richtext/actions/workflows/test.yml)

An alternative Wagtail `richtext` filter that can be configured in your apps settings.

It can parse the content in a RichText field in the same way the Wagtail richtext filter works and add classes or inline styles to the HTML.

Once the package is added to your Wagtail site, add one or two pieces of configuration to your settings then use the `f_richtext` template tag where you want the css classes or inline styles added to the HTML content.

 It's especially useful if you are including a CSS framework such as:

- [Bulma](https://bulma.io)
- [CodyHouse](https://codyhouse.co)
- [Tachyons](https://tachyons.io)
- [Tailwind](https://tailwindcss.com)
- other frameworks are available :)

## Installation

Install the package into your python environment.

```bash
pip install wagtail-f-richext
```

Add the package to your INSTALLED_APS

```python
"wagtail_f_richtext"
```

Any css framework styles will need to be installed before you will see any style changes for richtext content. If you are using only the inline styles you should see the effect of them applied when a page is viewed.

## Using the f_richtext filter

### with a RichText field

- `{{ page.body|f_richtext:"framework" }}` will add classes to the HTML tags
- `{{ page.body|f_richtext:"inline_styles" }}` will add inline styles to the HTML tags

### with a RichText block

- `{{ value|f_richtext:"framework" }}` will add classes to the HTML tags
- `{{ value|f_richtext:"inline_styles" }}` will add inline styles to the HTML tags

*You can use it without a parameter `{{ page.body|f_richtext }}` and it will work just like the Wagtail core provided filter (not required)*

## Configuration

You need to add one or both of `F_RICHTEXT_FRAMEWORK_CONFIG` or `F_RICHTEXT_INLINE_CONFIG` to your apps settings.

### Example for adding classes to HTML tags

```python
F_RICHTEXT_FRAMEWORK_CONFIG = {
    # target html tags
    "classes": {
        "h1": "heading-1",
        "h2": "heading-2",
        "ul": "list list--ul",
        "ol": "list list--ol",
        "a": "color-contrast-higher",
        "b": "font-bold",
        "i": "font-italic",
    },
    # wrap the richtext content with a class
    "wrapper_classes": [
        "text-component",
    ],
    # swap the richtext image alignment classes
    "alignment_classes": {
        "richtext-image left": "f-richtext-image f-richtext-image--left",
        "richtext-image right": "f-richtext-image f-richtext-image--right",
        "richtext-image full-width": "margin: 1em 0; width: 100%; height: auto;",
    },
    # remove any empty HTML tags (blank lines in the richtext editor)
    "remove_empty_tags": [
        "p",
    ],
    # add a clearfix to the end of the content
    "append_clearfix": True,
}
```

### Example for adding inline styles

```python
F_RICHTEXT_INLINE_CONFIG = {
    # target html tags
     "styles": {
        "h1": "margin-bottom: 1em;",
        "h2": "margin-bottom: 1em;",
        "h3": "margin-bottom: 1em;",
        "h4": "margin-bottom: 1em;",
        "h5": "margin-bottom: 1em;",
        "h6": "margin-bottom: 1em;",
        "p": "margin-bottom: 1em;",
        "ul": "float: none; clear: both; list-style: disc; margin-left: 2em; margin-bottom: 1em;",
        "ol": "float: none; clear: both; list-style: decimal; margin-left: 2em; margin-bottom: 1em;",
        "code": "font-family: monospace; background-color: #f5f5f5; padding: 0.25rem 0.5rem;",
        "sub": "vertical-align: sub; font-size: smaller;",
        "sup": "vertical-align: super; font-size: smaller;",
        "div": "float: none; clear: both;",
        "iframe": "max-width: 100%; width: 720px; height: 400px; margin-top: 1em; margin-bottom: 1em;",
        "b": "font-weight: bold;",
        "i": "font-style: italic;",
    },
    # wrap the richtext content with a style
    "wrapper_styles": [
        "overflow:hidden;",
    ],
    # swap the richtext image alignment classes for an inline style
    "alignment_styles": {
        "richtext-image left": "float: left; margin-right: 1rem; margin-left: 0; margin-bottom: 1rem; height: auto;",
        "richtext-image right": "float: right; margin-left: 1rem; margin-right: 0; margin-bottom: 1rem; height: auto;",
        "richtext-image full-width": "margin: 1em 0; width: 100%; height: auto;",
    },
    # remove any empty HTML tags (blank lines in the richtext editor)
    "remove_empty_tags": [
        "p",
    ],
    # add a clearfix to the end of the content
    "append_clearfix": True,
}
```

## Optional usage

### Use your own parser class

The parser class can be extended to add your own parsing requirements.

Create your own class that inherits from [fRichTextParser](./wagtail_f_richtext/parser.py) and add the following to your apps settings.

```python
F_RICHTEXT_PARSER_CLASS="the.dotted.path.to.your.own.Class"
```

### Use your own runner function

The order of the parsing and loading of your configuration is done in the runner method that is called by the `f_richtext` filter.

Create your own [runner function](./wagtail_f_richtext/parser.py#L102) in a suitable place and add the following settings to your app.

```python
F_RICHTEXT_PARSER_RUNNER="the.dotted.path.to.your.own.function"
```

## Contributing

The test app can be run easily to develop your contribution.

Fork the repo and clone it to your computer.

Change to the folder where you cloned it to.

With [poetry](https://python-poetry.org) installed run:

```bash
poetry install
poetry shell
make migrate
make loaddata
make run
```

Then you can view the app at <http://localhost:8000> and login to the admin at <http://localhost:8000/admin>

The admin account login is Username: `admin` Password: `password`

Run the test:

```bash
make test
```
