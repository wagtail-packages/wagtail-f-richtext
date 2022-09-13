from django.conf import settings
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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if hasattr(settings, "CSS_CDN_URL"):
            context["css_cdn_url"] = settings.CSS_CDN_URL
        else:
            context["css_cdn_url"] = ""
        return context


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

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        if hasattr(settings, "CSS_CDN_URL"):
            context["css_cdn_url"] = settings.CSS_CDN_URL
        else:
            context["css_cdn_url"] = ""
        return context
