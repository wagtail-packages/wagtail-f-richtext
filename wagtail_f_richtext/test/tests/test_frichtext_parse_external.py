from bs4 import BeautifulSoup
from django.test import TestCase, override_settings
from wagtail_f_richtext.templatetags.frichtext_tags import parse_external


class TestExternalStyleClasses(TestCase):
    @override_settings(
        F_RICHTEXT_EXTERNAL_CONFIG={
            "add_classes": {
                "ul": "foo-ul",
                "ol": "foo-ol",
                "a": "foo-link",
                "b": "foo-bold",
                "i": "foo-italic",
            }
        }
    )
    def test_parse_external_add_classes(self):
        output = parse_external(
            """
            <ul><li>List Item</li></ul>
            <ol><li>List Item</li></ol>
            <a href="http://foo.com">Bar</a>
            <b>Bold</b>
            <i>Italic</i>
            """
        )
        soup = BeautifulSoup(output, "html.parser")

        self.assertTrue(soup.find("ul", {"class": "foo-ul"}))
        self.assertTrue(soup.find("ol", {"class": "foo-ol"}))
        self.assertTrue(soup.find("a", {"class": "foo-link"}))
        self.assertTrue(soup.find("b", {"class": "foo-bold"}))
        self.assertTrue(soup.find("i", {"class": "foo-italic"}))

    @override_settings(
        F_RICHTEXT_EXTERNAL_CONFIG={
            "image_alignment_styles": {
                "richtext-image left": "foo-left",
                "richtext-image right": "bar-right",
                "richtext-image full-width": "baz-full-width",
            },
        }
    )
    def test_parse_external_image_alignment_styles(self):
        output = parse_external(
            """
            <img src="http://foo.com/bar.jpg" alt="Bar" class="richtext-image left" />
            <img src="http://foo.com/bar.jpg" alt="Bar" class="richtext-image right" />
            <img src="http://foo.com/bar.jpg" alt="Bar" class="richtext-image full-width" />
            """
        )
        soup = BeautifulSoup(output, "html.parser")

        self.assertTrue(soup.find("img", {"class": "foo-left"}))
        self.assertTrue(soup.find("img", {"class": "bar-right"}))
        self.assertTrue(soup.find("img", {"class": "baz-full-width"}))

    @override_settings(
        F_RICHTEXT_EXTERNAL_CONFIG={"remove_empty_tags": ["p", "b", "i", "div"]}
    )
    def test_parse_external_remove_empty_tags(self):
        output = parse_external(
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
        F_RICHTEXT_EXTERNAL_CONFIG={
            "append_clearfix_classes": True,
        }
    )
    def test_parse_external_append_clearfix_classes(self):
        output = parse_external(
            """
            <p class="foo">Sample</p>
            <p class="bar">Sample</p>
            """
        )
        soup = BeautifulSoup(output, "html.parser")

        self.assertTrue(soup.findAll(attrs={"style": "clear: both;"}))

    @override_settings(
        F_RICHTEXT_EXTERNAL_CONFIG={
            "append_clearfix_classes": False,
        }
    )
    def test_parse_external_append_clearfix_classes_false(self):
        output = parse_external(
            """
            <p class="foo">Sample</p>
            <p class="bar">Sample</p>
            """
        )
        soup = BeautifulSoup(output, "html.parser")

        self.assertFalse(soup.findAll(attrs={"style": "clear: both;"}))

    @override_settings(
        F_RICHTEXT_EXTERNAL_CONFIG={
            "wrapper_classes": ["foo bar baz"],
        }
    )
    def test_parse_external_wrapper(self):
        output = parse_external("""Any text""")
        soup = BeautifulSoup(output, "html.parser")

        self.assertTrue(soup.find("div", {"class": "foo bar baz"}))
