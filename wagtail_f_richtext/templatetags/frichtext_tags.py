from bs4 import BeautifulSoup
from django import template
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from wagtail.core.rich_text import RichText, expand_db_html

register = template.Library()


@register.filter
def f_richtext(value, format=None):

    if isinstance(value, RichText):
        # RichtextBlock
        if format == "internal":
            return parse_internal(value)
        elif format == "external":
            return parse_external(value)
        else:
            return value
    elif value is None:
        html = ""
    elif isinstance(value, str):
        # String from template filter
        db_html = expand_db_html(value)
        if format == "internal":
            html = parse_internal(db_html)
        elif format == "external":
            html = parse_external(db_html)
        else:
            html = db_html
    else:
        raise TypeError(
            "'f_richtext' template filter received an invalid value; expected string, got {}.".format(
                type(value)
            )
        )
    return render_to_string("wagtailcore/shared/richtext.html", {"html": html})


def parse_internal(html):
    """
    Parse a string of HTML and add classes and inline styles to tags.

    Returns
        string:
        The original HTML with classes and styles added.

    """
    config = getattr(settings, "F_RICHTEXT_INTERNAL_CONFIG", {})

    soup = BeautifulSoup(str(html), "html.parser")

    # Classes for wrapper HTML tag
    css_classes = (
        " ".join(config.get("wrapper_classes")) if config.get("wrapper_classes") else ""
    )

    # Add inline styles to HTML tags
    for tag, css_style in (
        config.get("add_tag_styles").items() if config.get("add_tag_styles") else []
    ):
        for element in soup.find_all(tag):
            element["style"] = css_style

    # Add inline styles to img HTML tags
    for tag, style in (
        config.get("image_alignment_styles").items()
        if config.get("image_alignment_styles")
        else []
    ):
        for element in soup.find_all("img", {"class": tag}):
            element["style"] = style

    # Add div HTML tag with clear style before aligned images
    for tag, style in (
        config.get("image_alignment_prepend_clear_floats").items()
        if config.get("image_alignment_prepend_clear_floats")
        else []
    ):
        for element in soup.find_all("img", {"class": tag}):
            element.insert_before(soup.new_tag("div", style=style))

    # Add clear float inline styles
    # for tag, style in (
    #     config.get("clear_float_styles").items()
    #     if config.get("clear_float_styles")
    #     else []
    # ):
    #     for element in soup.find_all(tag):
    #         element["style"] = style

    # Remove empty tags
    for tag in (
        config.get("remove_empty_tags") if config.get("remove_empty_tags") else []
    ):
        for element in soup.find_all(tag):
            if not element.contents:
                element.decompose()

    # Append a clear float div to the end of the content
    soup.append(soup.new_tag("div", style="clear: both;")) if config.get("append_clear_float") else None

    return mark_safe(f'<div class="{css_classes}">{str(soup)}</div>')


def parse_external(html):
    """
    Parse a string of HTML and add classes to HTML tags.

    Returns
        string:
        The original HTML with classes added.

    """
    config = getattr(settings, "F_RICHTEXT_EXTERNAL_CONFIG", {})

    soup = BeautifulSoup(str(html), "html.parser")

    # Classes for wrapper HTML tag
    css_classes = (
        " ".join(config.get("wrapper_classes")) if config.get("wrapper_classes") else ""
    )

    # Add classes to HTML tags
    for tag, css_class in (
        config.get("add_classes").items() if config.get("add_classes") else []
    ):
        for element in soup.find_all(tag):
            element["class"] = css_class

    # Add classes to img HTML tags
    for tag, css_class in (
        config.get("image_alignment_styles").items()
        if config.get("image_alignment_styles")
        else []
    ):
        for element in soup.find_all("img", {"class": tag}):
            element["class"] = css_class

    # Remove empty HTML tags
    for tag in (
        config.get("remove_empty_tags") if config.get("remove_empty_tags") else []
    ):
        for element in soup.find_all(tag):
            if not element.contents:
                element.decompose()

    # Append a clear float div to the end of the content
    soup.append(soup.new_tag("div", style="clear: both;")) if config.get(
        "append_clearfix_classes"
    ) else None

    return mark_safe(f'<div class="{css_classes}">{str(soup)}</div>')
