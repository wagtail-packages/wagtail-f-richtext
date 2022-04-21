from django.test import TestCase, override_settings
from wagtail_f_richtext.templatetags.frichtext_tags import (
    f_richtext,
    parse_external,
    parse_internal,
)
from bs4 import BeautifulSoup

HTML_INPUT = """<p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
<p></p>
<div></div>"""

HTML_OUTPUT = """
<div class="f-richtext external text-component">
<p>Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.</p>
<p></p>
<div></div>
</div>"""


class TestFRichtextTags(TestCase):
    @override_settings(
        F_RICHTEXT_EXTERNAL_CONFIG={
            "add_classes": {
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
                "p","div",
            ],
        }
    )
    def test_parse_external(self):
        output = parse_external(HTML_INPUT)
        soup = BeautifulSoup(output, "html.parser")
        print(soup.prettify())

        self.assertEqual(len(soup.find_all("p")), 1)
        self.assertEqual(len(soup.find_all("div")), 2)
        self.assertEqual(len(soup.find_all("div.f-richtext external text-component")), 1)