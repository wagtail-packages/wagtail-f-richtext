from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.module_loading import import_string
from wagtail.rich_text import RichText, expand_db_html

from wagtail_f_richtext.parser import fRichTextParser

register = template.Library()


@register.filter
def f_richtext(value, format=None):
    """
    This is a custom version of the Wagtail core richtext filter.

    Filter to render a RichText value as HTML, with formatting applied according to the
    F_RICHTEXT_FRAMEWORK_CONFIG or F_RICHTEXT_INLINE_CONFIG settings.

    Args:
        value (RichText): The RichText value to render.
        format (str): The format to render the value in. Defaults to None.

    Returns:
        str: The rendered HTML.

        Raises:
            TypeError: If value is not a RichText value.
    """
    html = value

    if hasattr(settings, "F_RICHTEXT_PARSER_CLASS"):
        parser_class = import_string(settings.F_RICHTEXT_PARSER_CLASS)
    else:
        parser_class = fRichTextParser

    if hasattr(settings, "F_RICHTEXT_PARSER_RUNNER"):
        parser_runner = import_string(settings.F_RICHTEXT_PARSER_RUNNER)
    else:
        parser_runner = import_string("wagtail_f_richtext.parser.parser_runner")

    if isinstance(value, RichText):
        # ditto: passing a RichText value through the |richtext filter should have no effect
        if format:
            runner = parser_runner(value, format=format, parser_class=parser_class)
            html = runner.do_wrapper(runner.config)
        else:
            return html
    elif value is None:
        html = ""
    elif isinstance(value, str):
        # String from template filter
        db_html = expand_db_html(value)
        if format:
            runner = parser_runner(db_html, format=format, parser_class=parser_class)
            html = runner.do_wrapper(runner.config)
        else:
            html = db_html
    else:
        raise TypeError(
            f"'f_richtext' template filter received an invalid value; expected string, got {type(value)}."
        )

    return render_to_string("wagtailcore/shared/richtext.html", {"html": html})
