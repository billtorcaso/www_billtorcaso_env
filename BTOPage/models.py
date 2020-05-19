from django.db import models
###from .utils import BTOInfoSnippet


from wagtail.core.blocks import (
    CharBlock,
    RichTextBlock,
    PageChooserBlock,
)
from wagtail.core.fields import StreamField
from wagtail.core.models import Page

from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.models import register_snippet

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, PageChooserPanel

from wagtail.images.models import Image
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel


@register_snippet
class BTOInfoSnippet(models.Model):
    """
    An InfoSnippet is a 4-tuple of (image, caption, info, link).
    It is typically used in CSS within an unordered list, in a way 
    that makes a responsive display of many InfoSnippets.
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
        PageChooserPanel("link_page"),
    ]


class BTOPage(Page):
    background_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    author = models.CharField(max_length=64, default="William D. Torcaso",
        null=True,
        blank=True,)
    body = StreamField(
        [
            ("heading", CharBlock(classname="full title")),
            ("rtblock", RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        null=True,
        blank=True,
    )
    info_stream = StreamField([("info_snippet", SnippetChooserBlock(BTOInfoSnippet))],
        null=True,
        blank=True,)
    template = "BTOPage/bto_responsive_page_v2.html"

    content_panels = Page.content_panels + [
        ImageChooserPanel("background_image"),
        FieldPanel("author"),
        StreamFieldPanel("body"),
        StreamFieldPanel("info_stream"),
    ]


###class BTOResponsivePage(BTOPage):
###    """
###    A ResponsivePage is an experiment in the CSS to make
###    a BTOPage responsive.  It may collapse back into BTOPage
###    when the experiment is done.
###    """
###
###    info_stream = StreamField([("info_snippet", SnippetChooserBlock(BTOInfoSnippet))],
###        null=True,
###        blank=True,)
###    template = "BTOPage/bto_responsive_page_v2.html"
###
###    content_panels = BTOPage.content_panels + [
###        StreamFieldPanel("info_stream"),
###    ]
###
###
