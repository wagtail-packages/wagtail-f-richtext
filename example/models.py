from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page


class FRichTextPage(Page):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class FRichTextPageStreamField(Page):
    body = StreamField(
        blocks.StreamBlock(
            [
                ("rich_text", blocks.RichTextBlock(template = "blocks/f_richtext_block.html")),
            ]
        )
    )

    content_panels = Page.content_panels + [
        StreamFieldPanel("body"),
    ]
