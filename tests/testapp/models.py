from django.conf import settings
from wagtail import VERSION as WAGTAIL_VERSION

if WAGTAIL_VERSION >= (3, 0):
    from wagtail import blocks
    from wagtail.admin.panels import FieldPanel
    from wagtail.fields import RichTextField, StreamField
    from wagtail.models import Page
else:
    from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
    from wagtail.core import blocks
    from wagtail.core.fields import RichTextField, StreamField
    from wagtail.core.models import Page


class BasePage(Page):
    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if hasattr(settings, "CSS_CDN_URL"):
            context["css_cdn_url"] = settings.CSS_CDN_URL
        else:
            context["css_cdn_url"] = ""
        return context

    class Meta:
        abstract = True


class HomePage(Page):
    template = "home_page.html"


class FRichTextPage(BasePage):
    template = "rich_text.html"
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]


class FRichTextPageStreamField(BasePage):
    template = "stream_field.html"
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

    content_panels = Page.content_panels + [
        FieldPanel("body") if WAGTAIL_VERSION >= (3, 0) else StreamFieldPanel("body")
    ]
