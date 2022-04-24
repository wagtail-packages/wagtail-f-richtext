from bs4 import BeautifulSoup
from django.test import TestCase

class TestFrichtextFilterStreamField(TestCase):

    fixtures = ["test_data.json"]

    def setUp(self):
        self.response = self.client.get("/f-rich-text-streamfield/")
        self.soup = BeautifulSoup(self.response.content, "html.parser")

    def test_frichtext_filter_raw(self):
        """ {{ value }} """
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

    def test_frichtext_filter_html(self):
        """ {{ value|f_richtext }} """
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

    def test_frichtext_filter_internal(self):
        """ {{ value|f_richtext:"internal" }} """
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

    def test_frichtext_filter_external(self):
        """ {{ value|f_richtext:"external" }} """
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