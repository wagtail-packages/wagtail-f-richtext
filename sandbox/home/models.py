from wagtail.admin.panels import FieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.models import Page


class HomePage(Page):
    pass


class FRichTextPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class FRichTextPageStreamField(Page):
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

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]
