from wagtail.models import Page
from wagtail.core.fields import RichTextField, StreamField
from wagtail import blocks


class HomePage(Page):
    body = RichTextField(blank=True)


class FRichTextPage(Page):
    body = RichTextField(blank=True)


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
