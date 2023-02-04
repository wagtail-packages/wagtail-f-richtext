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

Sample `framework` rendered

```html
<div class="text-component">
    <p data-block-key="92eli">A paragraph <b class="font-bold">Vulputate Vestibulum</b> <i class="font-italic">Commodo</i></p>
    <h2 class="heading-2" data-block-key="fkden">Heading 2</h2>
    <ul class="list list--ul">
        <li data-block-key="fe5cv">UL List Item 1</li>
        <li data-block-key="6ort3">UL List Item 2</li>
    </ul>
    <ol class="list list--ol">
        <li data-block-key="d5s3r">OL List Item 1</li>
        <li data-block-key="5l47j">OL List Item 2</li>
    </ol>
    <img alt="IMG_4511" class="f-richtext-image f-richtext-image--right" height="375" src="/media/images/IMG_4511.width-500.jpg" width="500">
    <div style="clear: both;"></div>
</div>
```

Sample `inline_styles` rendered

```html
<div style="overflow:hidden;">
    <p data-block-key="92eli" style="margin-bottom: 1em;">A paragraph <b style="font-weight: bold;">Vulputate Vestibulum</b> <i style="font-style: italic;">Commodo</i></p>
    <h2 data-block-key="fkden" style="margin-bottom: 1em;">Heading 2</h2>
    <ul style="float: none; clear: both; list-style: disc; margin-left: 2em; margin-bottom: 1em;">
        <li data-block-key="fe5cv">UL List Item 1</li>
        <li data-block-key="6ort3">UL List Item 2</li>
    </ul>
    <ol style="float: none; clear: both; list-style: decimal; margin-left: 2em; margin-bottom: 1em;">
        <li data-block-key="d5s3r">OL List Item 1</li>
        <li data-block-key="5l47j">OL List Item 2</li>
    </ol>
    <img alt="IMG_4511" class="richtext-image right" height="375" src="/media/images/IMG_4511.width-500.jpg" style="float: right; margin-left: 1rem; margin-right: 0; margin-bottom: 1rem; height: auto;" width="500">
    <div style="clear: both;"></div>
</div>
```

## Configuration

You need to add one or both of these settings to your apps settings.

- `F_RICHTEXT_FRAMEWORK_CONFIG`
- `F_RICHTEXT_INLINE_CONFIG`

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

The test app can be run to develop your contribution.

1. Fork the repo and clone it to your computer.
2. Change to the folder where you cloned it to.

With [poetry](https://python-poetry.org) installed run:

```bash
poetry install
poetry shell
# run the migrations, add an admin account and start the app
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Then you can view the app at <http://localhost:8000> and login to the admin at <http://localhost:8000/admin>

Run the tests:

```bash
python manage.py test
```

You can use shortcuts in the [Makefile](./Makefile) to run the above commands.
