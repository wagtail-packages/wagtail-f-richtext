from bs4 import BeautifulSoup as bs
from django.test import SimpleTestCase, override_settings

from wagtail_f_richtext.parser import fRichTextParser


class TestParser(SimpleTestCase):
    """
    Test the parser
    """

    def test_parser_available(self):
        """
        Test that the parser is available
        """
        self.assertTrue(fRichTextParser)

    def test_parser_raises_value_error_if_config_not_provided(self):
        """
        Test that the parser raises a ValueError if config is not provided
        """
        with self.assertRaises(ValueError):
            fRichTextParser(html="")

    def test_parser_can_be_created(self):
        """
        Test that the parser can be created
        """
        parser = fRichTextParser(html="", config_name="foo")
        self.assertIsInstance(parser, fRichTextParser)

    def test_parser_soup(self):
        """
        Test that the parser creates a soup object
        """
        parser = fRichTextParser(html="<p>foo bar baz</p>", config_name="foo")
        self.assertTrue(parser.soup, msg="Expected: <p>foo bar baz</p>")
        self.assertEqual(parser.soup.text, "foo bar baz", msg="Expected: foo bar baz")

    @override_settings(CONFIG={"foo": {}})
    def test_parser_config(self):
        """
        Test that the parser creates a config object
        """
        parser = fRichTextParser(html="foo bar baz", config_name="CONFIG")
        self.assertTrue(parser.config, msg="Expected: a dict")

    def test_parser_tag_cleaner_defaults(self):
        """
        Test that the parser tag cleaner defaults to p, div, span, ul, ol, li
        and removes empty tags
        """
        good_tags = [
            "<p>foo bar baz</p>",
            "<div>foo bar baz</div>",
            "<span>foo bar baz</span>",
            "<ul>foo bar baz</ul>",
            "<ol>foo bar baz</ol>",
            "<li>foo bar baz</li>",
        ]
        empty_tags = [
            "<p class='empty'></p>",
            "<div class='empty'></div>",
            "<span class='empty'></span>",
            "<ul class='empty'></ul>",
            "<ol class='empty'></ol>",
            "<li class='empty'></li>",
        ]
        empty_child_tags = [
            '<ul class="check"><li>foo bar baz</li><li class="empty-child"></li></ul>',
        ]
        html = "".join(good_tags + empty_tags + empty_child_tags)

        parser = fRichTextParser(html=html, config_name="foo")
        parser.tag_cleaner()  # call the method

        good_soup = bs(html, "html.parser").text  # get just the text from the soup
        self.assertEqual(parser.soup.text, good_soup, msg="Expected: foo bar baz")

        for tag in empty_tags:
            self.assertNotIn(
                tag, str(parser.soup), msg="Expected: empty tags are removed"
            )

        soup = parser.soup.find("ul", class_="check")
        li_count = len(soup.find_all("li"))
        self.assertEqual(li_count, 1, msg="Expected: empty child tags are removed")

    def test_parser_do_clear_fix(self):
        """
        Test that the parser can add a clear fix
        """
        parser = fRichTextParser(html="<p>foo bar baz</p>", config_name="foo")
        parser.do_clear_fix()

        soup = parser.soup.find("div", style="clear: both;")
        self.assertTrue(soup, msg='Expected: <div style="clear: both;""></div> exists')

    @override_settings(CONFIG={"wrapper_classes": ["foo", "bar"]})
    def test_parser_do_wrapper_classes(self):
        """
        Test that the parser can add wrapper classes
        """
        parser = fRichTextParser(html="<p>foo bar baz</p>", config_name="CONFIG")
        wrapped = parser.do_wrapper(parser.config)

        soup = bs(wrapped, "html.parser")
        wrapper_div = soup.find("div", class_="foo bar")
        self.assertTrue(wrapper_div, msg='Expected: <div class="foo bar"></div> exists')

    @override_settings(CONFIG={"wrapper_classes": ["foo"]})
    def test_parser_do_wrapper_classes_values(self):
        """
        Test that the parser can add wrapper classes with alternative passed in values
        """
        parser = fRichTextParser(html="<p>foo bar baz</p>", config_name="CONFIG")
        wrapped = parser.do_wrapper(parser.config, values=["bar"])

        soup = bs(wrapped, "html.parser")
        wrapper_div = soup.find("div", class_="bar")
        self.assertTrue(wrapper_div, msg='Expected: <div class="bar"></div> exists')

    @override_settings(CONFIG={"wrapper_styles": ["overflow: hidden;", "clear: both;"]})
    def test_parser_do_wrapper_styles(self):
        """
        Test that the parser can add wrapper styles
        """
        parser = fRichTextParser(html="<p>foo bar baz</p>", config_name="CONFIG")
        wrapped = parser.do_wrapper(parser.config)

        soup = bs(wrapped, "html.parser")
        wrapper_div = soup.find("div", style="overflow: hidden; clear: both;")
        self.assertTrue(
            wrapper_div,
            msg='Expected: <div style="overflow: hidden; clear: both;"></div> exists',
        )

    @override_settings(CONFIG={"wrapper_styles": ["overflow: hidden;"]})
    def test_parser_do_wrapper_styles_values(self):
        """
        Test that the parser can add wrapper styles with alternative passed in values
        """
        parser = fRichTextParser(html="<p>foo bar baz</p>", config_name="CONFIG")
        wrapped = parser.do_wrapper(parser.config, values=["clear: both;"])

        soup = bs(wrapped, "html.parser")
        wrapper_div = soup.find("div", style="clear: both;")
        self.assertTrue(
            wrapper_div, msg='Expected: <div style="clear: both;"></div> exists'
        )

    @override_settings(CONFIG={"classes": {"h1": "foo", "h2": "bar"}})
    def test_parser_do_style_tags_default_framework(self):
        """
        Test that the parser can add classes to tags from framework type config
        External type config leads to classes being added to tags
        """
        html = [
            "<h1>foo bar baz</h1>",
            "<h2>foo bar baz</h2>",
        ]
        parser = fRichTextParser(html=html, config_name="CONFIG")
        parser.do_style_tags(values=parser.config["classes"])

        soup = parser.soup.find("h1", class_="foo")
        self.assertTrue(soup, msg='Expected: <h1 class="foo"></h1> exists')

        soup = parser.soup.find("h2", class_="bar")
        self.assertTrue(soup, msg='Expected: <h2 class="bar"></h2> exists')

    @override_settings(CONFIG={"classes": {"h1": "foo", "h2": "bar"}})
    def test_parser_do_style_tags_default_framework_values(self):
        """
        Test that the parser can add classes to tags from framework type config
        when alternative passed in values are used
        """
        html = [
            "<h1>foo bar baz</h1>",
            "<h2>foo bar baz</h2>",
        ]
        parser = fRichTextParser(html=html, config_name="CONFIG")
        parser.do_style_tags(values={"h1": "bax", "h2": "qux"})

        # make sure the config values are not used
        soup = parser.soup.find("h1", class_="foo")
        self.assertFalse(soup, msg='Expected: <h1 class="foo"></h1> does not exist')

        # make sure the passed in values are used
        soup = parser.soup.find("h1", class_="bax")
        self.assertTrue(soup, msg='Expected: <h1 class="bax"></h1> exists')
        soup = parser.soup.find("h2", class_="qux")
        self.assertTrue(soup, msg='Expected: <h2 class="qux"></h2> exists')

    @override_settings(CONFIG={"styles": {"h1": "font-size: normal;"}})
    def test_parser_do_style_tags_raises_exception(self):
        """
        Test that the parser raises an exception when the format is not valid
        """
        parser = fRichTextParser(html="", config_name="CONFIG", format="invalid")
        with self.assertRaises(ValueError):
            parser.do_style_tags(values=parser.config["styles"])

    @override_settings(
        CONFIG={
            "styles": {
                "h1": "font-size: normal;",
                "h2": "margin-top: 0;",
                "ul": "list-style: none;",
            }
        }
    )
    def test_parser_do_style_tags_default_inline_styles(self):
        """
        Test that the parser can add styles to tags from inline_styles type config
        Internal type config leads to styles being added to tags
        """
        html = [
            "<h1>foo bar baz</h1>",
            "<h2>foo bar baz</h2>",
            "<ul><li>foo</li><li>bar</li><li>baz</li></ul>",
        ]
        parser = fRichTextParser(
            html=html, config_name="CONFIG", format="inline_styles"
        )
        parser.do_style_tags(values=parser.config["styles"])

        soup = parser.soup.find("h1", style="font-size: normal;")
        self.assertTrue(
            soup, msg='Expected: <h1 style="font-size: normal;"></h1> exists'
        )

        soup = parser.soup.find("h2", style="margin-top: 0;")
        self.assertTrue(soup, msg='Expected: <h2 style="margin-top: 0;"></h2> exists')

        soup = parser.soup.find("ul", style="list-style: none;")
        self.assertTrue(
            soup, msg='Expected: <ul style="list-style: none;"></ul> exists'
        )

    @override_settings(
        CONFIG={
            "classes": {
                "h1": "foo",
                "h2": "bar",
                "ul": "baz",
            }
        }
    )
    def test_parser_do_style_tags_default_framework_classes(self):
        """
        Test that the parser can add classes to tags from framework type config
        External type config leads to classes being added to tags
        """
        html = [
            "<h1>foo bar baz</h1>",
            "<h2>foo bar baz</h2>",
            "<ul><li>foo</li><li>bar</li><li>baz</li></ul>",
        ]
        parser = fRichTextParser(html=html, config_name="CONFIG", format="framework")
        parser.do_style_tags(values=parser.config["classes"])

        soup = parser.soup.find("h1", class_="foo")
        self.assertTrue(soup, msg='Expected: <h1 class="foo"></h1> exists')

        soup = parser.soup.find("h2", class_="bar")
        self.assertTrue(soup, msg='Expected: <h2 class="bar"></h2> exists')

        soup = parser.soup.find("ul", class_="baz")
        self.assertTrue(soup, msg='Expected: <ul class="baz"></ul> exists')

    @override_settings(
        CONFIG={
            "alignment_classes": {
                "richtext-image left": "left-aligned",
                "richtext-image right": "right-aligned",
            }
        }
    )
    def test_parser_do_style_images_default_framework(self):
        """
        Test that the parser can add classes to images from framework type config
        External type config leads to classes being added to images
        """
        html = [
            '<img src="foo.jpg" class="richtext-image left" />',
            '<img src="bar.jpg" class="richtext-image right" />',
        ]
        parser = fRichTextParser(html=html, config_name="CONFIG")
        parser.do_style_images(values=parser.config["alignment_classes"])

        soup = parser.soup.find("img", class_="left-aligned")
        self.assertTrue(soup, msg='Expected: <img class="left-aligned"></img> exists')

        soup = parser.soup.find("img", class_="right-aligned")
        self.assertTrue(soup, msg='Expected: <img class="right-aligned"></img> exists')

    @override_settings(
        CONFIG={
            "alignment_styles": {
                "richtext-image left": "float: left;",
                "richtext-image right": "float: right;",
            }
        }
    )
    def test_parser_do_style_images_default_inline_styles(self):
        """
        Test that the parser can add styles to images from inline_styles type config
        Internal type config leads to styles being added to images
        """
        html = [
            '<img src="foo.jpg" class="richtext-image left" />',
            '<img src="bar.jpg" class="richtext-image right" />',
        ]
        parser = fRichTextParser(
            html=html, config_name="CONFIG", format="inline_styles"
        )
        parser.do_style_images(values=parser.config["alignment_styles"])

        soup = parser.soup.find("img", style="float: left;")
        self.assertTrue(soup, msg='Expected: <img style="float: left;"></img> exists')

        soup = parser.soup.find("img", style="float: right;")
        self.assertTrue(soup, msg='Expected: <img style="float: right;"></img> exists')

    @override_settings(
        CONFIG={
            "alignment_classes": {
                "richtext-image left": "left-aligned",
                "richtext-image right": "right-aligned",
            }
        }
    )
    def test_parser_do_style_images_raises(self):
        """
        Test that the parser raises an exception when the format is not valid
        """
        html = [
            '<img src="foo.jpg" class="richtext-image left" />',
            '<img src="bar.jpg" class="richtext-image right" />',
        ]
        parser = fRichTextParser(html=html, config_name="CONFIG", format="invalid")
        with self.assertRaises(ValueError):
            parser.do_style_images(values=parser.config["alignment_classes"])
