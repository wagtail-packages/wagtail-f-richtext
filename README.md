# Wagtail F Richtext

[![test](https://github.com/nickmoreton/wagtail-f-richtext/actions/workflows/test.yml/badge.svg)](https://github.com/nickmoreton/wagtail-f-richtext/actions/workflows/test.yml)

An alternative Wagtail `richtext` filter.

Parse the HTML content from a RichText field or RichText Stream Field Block in the same way that the Wagtail richtext filter works.

Add an argument to specify either in-line styles or css classes to be injected to style the inner html content.

Use your own custom css classes or one the many other utility-first CSS frameworks like:

- [Bulma](https://bulma.io)
- [CodyHouse](https://codyhouse.co)
- [Tachyons](https://tachyons.io)
- [Tailwind](https://tailwindcss.com)
- other frameworks are available :)

## Setup / Installation

Install the package into your python environment.

```bash
pip install wagtail-f-richext
```

Add the package to your INSTALLED_APS

```python
"wagtail_f_richtext"
```

### Using it with a RichText field

- `{{ page.body|f_richtext }}` will work just like the Wagtail provided filter
- `{{ page.body|f_richtext:"external" }}` will add classes to the HTML tags
- `{{ page.body|f_richtext:"internal" }}` will add inline styles to the HTML tags

### Using it with a RichText field in a Stream Field Block

- `{{ value|f_richtext }}` will work just like the Wagtail provided filter
- `{{ value|f_richtext:"external" }}` will add classes to the HTML tags
- `{{ value|f_richtext:"internal" }}` will add inline styles to the HTML tags

## Configuration

Without any configuration added to your site settings nothing will be parsed so you need to add one or both of `F_RICHTEXT_INTERNAL_CONFIG` or `F_RICHTEXT_EXTERNAL_CONFIG`

### Example for adding inline styles

Use this to add inline styles attributes to the HTML tags.

```python
F_RICHTEXT_INTERNAL_CONFIG = {
    # target html tags and add in-line styles
    "add_tag_styles": {
        "h2": "margin-bottom: 1em; font-size: 4em; font-weight:400",
        "p": "margin-bottom: 1em;",
        "ul": "float: none; clear: both; list-style: disc; margin-left: 2em; margin-bottom: 1em;",
        "code": "font-family: monospace; background-color: #f5f5f5; padding: 0.25rem 0.5rem;",
        "b": "font-weight: bold; color: darkred;",
        "i": "font-style: italic; color: pink;",
    },
    # target the provided image alignment classes
    "image_alignment_styles": {
        "richtext-image left": "float: left; margin-right: 1rem; margin-left: 0; margin-bottom: 1rem; height: auto;",
        "richtext-image right": "float: right; margin-left: 1rem; margin-right: 0; margin-bottom: 1rem; height: auto;",
        "richtext-image full-width": "margin: 1em 0; width: 100%; height: auto;",
    },
    # and clear the floats above
    "image_alignment_prepend_clear_floats": {
        "richtext-image left": "clear: both;",
        "richtext-image right": "clear: both;",
        "richtext-image full-width": "clear: both;",
    },
    # clean up the empty tags (they can happen)
    "remove_empty_tags": [
        "p",
    ],
}
```

### Example for adding classes to HTML tags

Use this to add css classes to the HTML tags.

```python
F_RICHTEXT_EXTERNAL_CONFIG = {
    # target html tags and add css classes
    "add_classes": {
        "h2": "title",
        "a": "color-contrast-higher",
        "b": "font-bold",
        "i": "font-italic color-contrast-medium",
    },
    # some utility frameworks provide classes to wrap blocks of text content
    "wrapper_classes": [
        "text-component",
    ],
    # target the provided image alignment classes
    "image_alignment_styles": {
        "richtext-image left": "f-richtext-image f-richtext-image--left",
        "richtext-image right": "f-richtext-image f-richtext-image--right",
        "richtext-image full-width": "margin: 1em 0; width: 100%; height: auto;",
    },
    # and clear the floats above
    "clear_float_styles": {
        "ul": "list list--ul float-none clear-both;",
        "ol": "list list--ol float-none clear-both;",
    },
    # clean up the empty tags (they can happen)
    "remove_empty_tags": [
        "p",
    ],
}
```

## Examples

View the [Sandbox](/sandbox/) app for detailed example usage.

The sandbox app is fully configured and can be run with:

```bash
poetry install
poetry shell
make run
```
