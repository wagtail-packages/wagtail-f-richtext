from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import blocks
    from wagtail.fields import RichTextField, StreamField
    from wagtail.models import Page
else:
    from wagtail.core import blocks
    from wagtail.core.fields import RichTextField, StreamField
    from wagtail.core.models import Page


class HomePage(Page):
    body = RichTextField(blank=True)


class FRichTextPage(Page):
    body = RichTextField(blank=True)


class FRichTextPageStreamField(Page):
    if WAGTAIL_VERSION >= (3, 0):
        body = StreamField(
            blocks.StreamBlock(
                [
                    (
                        "rich_text",
                        blocks.RichTextBlock(template="blocks/f_richtext_block.html"),
                    ),
                ]
            ),
            use_json_field=True,
        )
    else:
        body = StreamField(
            [
                (
                    "rich_text",
                    blocks.RichTextBlock(template="blocks/f_richtext_block.html"),
                ),
            ]
        )
