from bs4 import BeautifulSoup
from django.test import TestCase, override_settings
from wagtail_f_richtext.templatetags.frichtext_tags import parse_internal


class TestIntrenalStyleArrs(TestCase):
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
            }
        }
    )
    def test_parse_internal_add_tag_styles(self):
        output = parse_internal(
            """
            <h1>Heading 1</h1>
            <h2>Heading 2</h2>
            <h3>Heading 3</h3>
            <h4>Heading 4</h4>
            <h5>Heading 5</h5>
            <h6>Heading 6</h6>
            <p>Paragraph</p>
            <ul>
                <li>List Item</li>
            </ul>
            <ol>
                <li>List Item</li>
            </ol>
            <code>Code</code>
            <sub>Sub</sub>
            <sup>Sup</sup>
            <iframe src="http://foo.com/bar.html"></iframe>
            """
        )
        soup = BeautifulSoup(output, "html.parser")

        self.assertTrue(soup.find("h1", {"style": "margin-bottom: 1em;"}))
        self.assertTrue(soup.find("h2", {"style": "margin-bottom: 1em;"}))
        self.assertTrue(soup.find("h3", {"style": "margin-bottom: 1em;"}))
        self.assertTrue(soup.find("h4", {"style": "margin-bottom: 1em;"}))
        self.assertTrue(soup.find("h5", {"style": "margin-bottom: 1em;"}))
        self.assertTrue(soup.find("h6", {"style": "margin-bottom: 1em;"}))
        self.assertTrue(soup.find("p", {"style": "margin-bottom: 1em;"}))
        self.assertTrue(
            soup.find(
                "ul",
                {
                    "style": "float: none; clear: both; list-style: disc; margin-left: 2em; margin-bottom: 1em;"
                },
            )
        )
        self.assertTrue(
            soup.find(
                "ol",
                {
                    "style": "float: none; clear: both; list-style: decimal; margin-left: 2em; margin-bottom: 1em;"
                },
            )
        )
        self.assertTrue(
            soup.find(
                "code",
                {
                    "style": "font-family: monospace; background-color: #f5f5f5; padding: 0.25rem 0.5rem;"
                },
            )
        )
        self.assertTrue(
            soup.find("sub", {"style": "vertical-align: sub; font-size: smaller;"})
        )
        self.assertTrue(
            soup.find("sup", {"style": "vertical-align: super; font-size: smaller;"})
        )

    @override_settings(
        F_RICHTEXT_INTERNAL_CONFIG={
            "image_alignment_styles": {
                "richtext-image left": "float: left; margin-right: 1rem;",
                "richtext-image right": "float: right; margin-left: 1rem;",
                "richtext-image full-width": "margin: 1em 0; width: 100%; height: auto;",
            },
            "image_alignment_prepend_clear_floats": {
                "richtext-image left": "clear: both;",
                "richtext-image right": "clear: both;",
                "richtext-image full-width": "clear: both;",
            },
        }
    )
    def test_parse_internal_image_alignment_styles(self):
        output = parse_internal(
            """
            <img src="http://foo.com/bar.jpg" class="richtext-image left">
            <img src="http://foo.com/bar.jpg" class="richtext-image right">
            <img src="http://foo.com/bar.jpg" class="richtext-image full-width">
            """
        )
        soup = BeautifulSoup(output, "html.parser")

        self.assertTrue(soup.find("img", {"style": "float: left; margin-right: 1rem;"}))
        self.assertTrue(soup.find("img", {"style": "float: right; margin-left: 1rem;"}))
        self.assertTrue(
            soup.find("img", {"style": "margin: 1em 0; width: 100%; height: auto;"})
        )
        self.assertTrue(len(soup.findAll(attrs={"style": "clear: both;"})) == 3)

    @override_settings(
        F_RICHTEXT_INTERNAL_CONFIG={"remove_empty_tags": ["p", "b", "i", "div"]}
    )
    def test_parse_internal_remove_empty_tags(self):
        output = parse_internal(
            """
            <p class="remains">Lorem Ipsum is simply dummy text and should remain in the output</p>
            <p class="removed"></p>
            <b class="removed"></b>
            <i class="removed"></i>
            <div class="remains">Lorem Ipsum is simply dummy text and should remain in the output</div>
            """
        )
        soup = BeautifulSoup(output, "html.parser")

        remaining_p = soup.find("p", {"class": "remains"})
        self.assertTrue(remaining_p)

        removed_p = soup.find("p", {"class": "removed"})
        self.assertFalse(removed_p)

        removed_b = soup.find("b", {"class": "removed"})
        self.assertFalse(removed_b)

        removed_i = soup.find("i", {"class": "removed"})
        self.assertFalse(removed_i)

        remaining_div = soup.find("div", {"class": "remains"})
        self.assertTrue(remaining_div)

    @override_settings(
        F_RICHTEXT_INTERNAL_CONFIG={
            "append_clear_float": True,
        }
    )
    def test_parse_internal_append_clearfix_classes(self):
        output = parse_internal(
            """
            <p class="foo">Sample</p>
            <p class="bar">Sample</p>
            """
        )
        soup = BeautifulSoup(output, "html.parser")

        self.assertTrue(soup.findAll(attrs={"style": "clear: both;"}))

    @override_settings(
        F_RICHTEXT_INTERNAL_CONFIG={
            "wrapper_classes": ["foo bar baz"],
        }
    )
    def test_parse_internal_wrapper(self):
        output = parse_internal("""Any text""")
        soup = BeautifulSoup(output, "html.parser")

        self.assertTrue(soup.find("div", {"class": "foo bar baz"}))
