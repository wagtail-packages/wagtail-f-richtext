from bs4 import BeautifulSoup
from django.conf import settings
from django.utils.safestring import mark_safe


class fRichTextParser:
    """
    Parse a string of HTML and add classes and inline styles to tags dependent on the configuration.

    Args:
        html (str): The HTML to parse.
        parser (str): The parser to use. Defaults to "html.parser".
        config_name (str): The name of the config to use. Defaults to None.

        Raises:
            ValueError: If config_name is not provided.
    """

    def __init__(
        self,
        html,
        format="framework",
        parser="html.parser",
        config_name=None,
    ):
        if not config_name:
            raise ValueError("Config must be provided.")

        self.soup = self._soup(html, parser)
        self.config = self._config(config_name)
        self.format = format

    @staticmethod
    def _soup(html, parser="html.parser"):
        # Create a BeautifulSoup object
        return BeautifulSoup(str(html), parser)

    @staticmethod
    def _config(config_name):
        return getattr(settings, config_name, {})

    def tag_cleaner(self, html_tags=None):
        html_tags = html_tags if html_tags else ["p", "div", "span", "ul", "ol", "li"]
        for tag in html_tags:
            for element in self.soup.find_all(tag):
                element.decompose() if not element.contents else None

    def do_clear_fix(self):
        self.soup.append(self.soup.new_tag("div", style="clear: both;"))

    def do_wrapper(self, config, html_tag="div", values=None):
        if config.get("wrapper_classes"):
            wrapper_attribute = "class"
            if not values:
                values = " ".join(config.get("wrapper_classes"))
            else:
                values = " ".join(values)  # uses the passed in values

        elif config.get("wrapper_styles"):
            wrapper_attribute = "style"
            if not values:
                values = " ".join(config.get("wrapper_styles"))
            else:
                values = " ".join(values)  # uses the passed in values

        return (
            mark_safe(
                f'<{html_tag} {wrapper_attribute}="{values}">{str(self.soup)}</{html_tag}>'
            )
            if values
            else mark_safe(str(self.soup))
        )

    def do_style_tags(self, values=None):
        values = values.items() if values else {}
        if self.format == "framework":
            for tag, css_class in values:
                for element in self.soup.find_all(tag):
                    element["class"] = css_class
        elif self.format == "inline_styles":
            for tag, css_style in values:
                for element in self.soup.find_all(tag):
                    element["style"] = css_style
        else:
            raise ValueError("Format must be 'framework' or 'inline_styles'.")

    def do_style_images(self, values=None):
        values = values.items() if values else {}

        if self.format == "framework":
            for original_class, new_class in values:
                for element in self.soup.find_all("img", {"class": original_class}):
                    element["class"] = new_class
        elif self.format == "inline_styles":
            for original_class, new_style in values:
                for element in self.soup.find_all("img", {"class": original_class}):
                    element["style"] = new_style
        else:
            raise ValueError("Format must be 'framework' or 'inline_styles'.")


def parser_runner(html, format=None, parser_class=None):
    """
    Run the parser.

    Args:
        html (str): The HTML to parse.
        format (str): The format to parse. Defaults to None.
        parser_class (class): The parser class to use. Defaults to None.

    Returns:
        parser (class): The parser class.

    Raises:
        ValueError: If format is not provided.
        ValueError: If parser_class is not provided.
    """

    config_name = (
        "F_RICHTEXT_FRAMEWORK_CONFIG"
        if format == "framework"
        else "F_RICHTEXT_INLINE_CONFIG"
    )
    parser = parser_class(html, format=format, config_name=config_name)

    if parser.config.get("remove_empty_tags"):
        # Remove empty tags
        parser.tag_cleaner(parser.config.get("remove_empty_tags"))

    if format == "framework":
        # Add classes to tags
        parser.do_style_tags(values=parser.config.get("classes"))
        parser.do_style_images(values=parser.config.get("alignment_classes"))

    if format == "inline_styles":
        # Add inline styles to tags
        parser.do_style_tags(values=parser.config.get("styles"))
        parser.do_style_images(values=parser.config.get("alignment_styles"))

    if parser.config.get("append_clearfix"):
        # Append a clear fix html element
        parser.do_clear_fix()

    return parser
