F_RICHTEXT_INTERNAL_CONFIG = {
    "add_tag_styles": {
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
    "image_alignment_styles": {
        "richtext-image left": "float: left; margin-right: 1rem; margin-left: 0; margin-bottom: 1rem; height: auto;",
        "richtext-image right": "float: right; margin-left: 1rem; margin-right: 0; margin-bottom: 1rem; height: auto;",
        "richtext-image full-width": "margin: 1em 0; width: 100%; height: auto;",
    },
    "image_alignment_prepend_clear_floats": {
        "richtext-image left": "clear: both;",
        "richtext-image right": "clear: both;",
        "richtext-image full-width": "clear: both;",
    },
    "remove_empty_tags": [
        "p",
    ],
}

### CODYHOUSE ###
F_RICHTEXT_EXTERNAL_CONFIG = {
    "add_classes": {
        "h2": "title",
        "ul": "list list--ul",
        "ol": "list list--ol",
        "a": "color-contrast-higher",
        "b": "font-bold",
        "i": "font-italic",
    },
    "wrapper_classes": [
        "text-component",
    ],
    "image_alignment_styles": {
        "richtext-image left": "f-richtext-image f-richtext-image--left",
        "richtext-image right": "f-richtext-image f-richtext-image--right",
        "richtext-image full-width": "margin: 1em 0; width: 100%; height: auto;",
    },
    "clear_float_styles": {
        "ul": "list list--ul float-none clear-both;",
        "ol": "list list--ol float-none clear-both;",
    },
    "remove_empty_tags": [
        "p",
    ],
}