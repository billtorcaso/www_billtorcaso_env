from django.db import models


from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core.blocks import (
    CharBlock,
    RichTextBlock,
    PageChooserBlock,
)
from wagtail.snippets.models import register_snippet

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, PageChooserPanel

from wagtail.images.models import Image
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel


class BTOPage(Page):
    background_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    author = models.CharField(max_length=64, default="William D. Torcaso")
    body = StreamField(
        [
            ("heading", CharBlock(classname="full title")),
            ("rtblock", RichTextBlock()),
            ("image", ImageChooserBlock()),
        ]
    )

    content_panels = Page.content_panels + [
        ImageChooserPanel("background_image"),
        FieldPanel("author"),
        StreamFieldPanel("body"),
    ]


class BTOResponsivePage(BTOPage):
    """
    A ResponsivePage is an experiment in the CSS to make
    a BTOPage responsive.  It may collapse back into BTOPage
    when the experiment is done.
    """

    template = "BTOPage/bto_responsive_page_v2.html"
    pass


@register_snippet
class BTOInfoSnippet(models.Model):
    """
    An InfoSnippet is a 4-tuple of (image, caption, info, link).
    It is typically used in an unordered list, in a way that makes
    a responsive display of many InfoSnippets.
    """

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    caption = models.CharField(max_length=80)
    info = RichTextBlock()
    link_page = PageChooserBlock(
        required=True, label="Internal Link", help_text="Required link to a page on BTO"
    )

    panels = [
        ImageChooserPanel("image"),
        FieldPanel("caption"),
        FieldPanel("info"),
        PageChooserPanel("image"),
    ]
