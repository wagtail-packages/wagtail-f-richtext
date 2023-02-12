from django.conf import settings
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField, StreamField
from wagtail.models import Page


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
    max_count = 1

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["child_pages"] = self.get_children().live()

        return context


class FRichTextPage(BasePage):
    body = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("body"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        context["child_pages"] = self.get_parent().get_children().live()

        return context


class FRichTextPageStreamField(BasePage):
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
        context["child_pages"] = self.get_parent().get_children().live()

        return context
