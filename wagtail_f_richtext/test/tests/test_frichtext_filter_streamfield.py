import json

from bs4 import BeautifulSoup
from django.test import TestCase, override_settings

from wagtail_f_richtext.test.models import FRichTextPageStreamField, HomePage


class TestFrichtextFilterStreamField(TestCase):

    STREAM_FIELD = [
        {
            "type": "rich_text",
            "value": """
                <h2>Heading 2</h2>\n
                <h3>Heading 3</h3>\n
                <h4>Heading 4</h4>\n
                <p>Paragraph. Paragraph. Paragraph. Paragraph. Paragraph.</p>\n
                <ul>\n
                <li>ul lits item</li>\n
                <li>ul lits item</li>\n
                <li>ul lits item</li>\n
                </ul>\n
                <ol>\n
                <li>ol list item</li>\n
                <li>ol list item</li>\n
                <li>ol list item</li>\n
                </ol>\n
                <p><b>Bold</b></p>\n
                <p><i>Italic</i></p>\n
                <p></p>
            """,
        }
    ]

    @override_settings(
        F_RICHTEXT_INTERNAL_CONFIG={
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
                "richtext-image left": "float: left; margin-right: 1rem; margin-left: 0; margin-bottom: 1rem; height: auto;",  # noqa: E501
                "richtext-image right": "float: right; margin-left: 1rem; margin-right: 0; margin-bottom: 1rem; height: auto;",  # noqa: E501
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
        },
        F_RICHTEXT_EXTERNAL_CONFIG={
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
        },
    )
    def setUp(self):
        self.home_page = HomePage.objects.first()
        rich_text_page = FRichTextPageStreamField(
            title="F Rich Text Streamfield Page", body=json.dumps(self.STREAM_FIELD)
        )
        self.home_page.add_child(instance=rich_text_page)
        rev = rich_text_page.save_revision()
        rev.publish()

        self.response = self.client.get("/f-rich-text-streamfield-page/")
        self.soup = BeautifulSoup(self.response.content, "html.parser")

    def test_frichtext_filter_raw(self):
        """{{ value }}
        the result should be untouched as no filter is applied"""
        richtext = self.soup.find("div", {"class": "test-raw"})
        # we should be able to parse it with BeautifulSoup
        self.assertTrue(richtext.find("h2"))
        self.assertTrue(richtext.find("p"))
        self.assertTrue(richtext.find("ul"))
        self.assertTrue(richtext.find("ol"))
        self.assertTrue(richtext.find("b"))
        self.assertTrue(richtext.find("i"))
        # expecting a <iframe> tag will not be found
        self.assertFalse(richtext.find("iframe"))
        # check if empty <p> tags are removed
        all_p_tags = richtext.findAll("p")
        self.assertEqual(len(all_p_tags), 4)

    def test_frichtext_filter_html(self):
        """{{ value|f_richtext }}
        the result should be untouched as no filter is applied"""
        richtext = self.soup.find("div", {"class": "test-frichtext"})
        # we should be able to parse it with BeautifulSoup
        self.assertTrue(richtext.find("h2"))
        self.assertTrue(richtext.find("p"))
        self.assertTrue(richtext.find("ul"))
        self.assertTrue(richtext.find("ol"))
        self.assertTrue(richtext.find("b"))
        self.assertTrue(richtext.find("i"))
        # expecting a <iframe> tag will not be found
        self.assertFalse(richtext.find("iframe"))
        # check if empty <p> tags are removed
        all_p_tags = richtext.findAll("p")
        self.assertEqual(len(all_p_tags), 4)

    def test_frichtext_filter_internal(self):
        """{{ value|f_richtext:"internal" }}
        the result should be modified to include style tags as internal is used"""
        richtext = self.soup.find("div", {"class": "test-frichtext-internal"})
        # we should be able to parse it with BeautifulSoup
        self.assertTrue(richtext.find("h2", {"style": "margin-bottom: 1em;"}))
        self.assertTrue(richtext.find("p", {"style": "margin-bottom: 1em;"}))
        self.assertTrue(
            richtext.find(
                "ul",
                {
                    "style": "float: none; clear: both; list-style: disc; margin-left: 2em; margin-bottom: 1em;"
                },
            )
        )
        self.assertTrue(
            richtext.find(
                "ol",
                {
                    "style": "float: none; clear: both; list-style: decimal; margin-left: 2em; margin-bottom: 1em;"
                },
            )
        )
        self.assertTrue(richtext.find("b", {"style": "font-weight: bold;"}))
        self.assertTrue(richtext.find("i", {"style": "font-style: italic;"}))
        # expecting a <iframe> tag will not be found
        self.assertFalse(richtext.find("iframe"))
        # check if empty <p> tags are removed
        all_p_tags = richtext.findAll("p")
        self.assertEqual(len(all_p_tags), 3)

    def test_frichtext_filter_external(self):
        """{{ value|f_richtext:"external" }}
        the result should be modified to include class tags as external is used"""
        richtext = self.soup.find("div", {"class": "test-frichtext-external"})
        # we should be able to parse it with BeautifulSoup
        self.assertTrue(richtext.find("h2", {"class": "title"}))
        self.assertTrue(richtext.find("p", {"class": None}))
        self.assertTrue(richtext.find("ul", {"class": "list list--ul"}))
        self.assertTrue(richtext.find("ol", {"class": "list list--ol"}))
        self.assertTrue(richtext.find("b", {"class": "font-bold"}))
        self.assertTrue(richtext.find("i", {"class": "font-italic"}))
        # expecting a <iframe> tag will not be found
        self.assertFalse(richtext.find("iframe"))
        # check if empty <p> tags are removed
        all_p_tags = richtext.findAll("p")
        self.assertEqual(len(all_p_tags), 3)
