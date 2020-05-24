from django.db import models
from wagtail.core.blocks import (
    CharBlock,
    PageChooserBlock,
    RichTextBlock,
    TextBlock,
)

from wagtail.core.blocks import TextBlock
from wagtail.core.fields import StreamField
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page

from wagtail.snippets.blocks import SnippetChooserBlock
from wagtail.snippets.models import register_snippet

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, PageChooserPanel

from wagtail.images.models import Image
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel


@register_snippet
class BTOInfoSnippet(models.Model):
    """ An InfoSnippet is a 3-tuple of (image, caption, info).  
        It is typically used in CSS within an unordered list, 
        in a way that makes a responsive display of many InfoSnippets.
    """

    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
    caption = models.CharField(max_length=80)
    info = models.CharField(
        max_length=256, default="William D. Torcaso", null=True, blank=True,
    )

    panels = [
        ImageChooserPanel("image"),
        FieldPanel("caption"),
        FieldPanel("info"),
    ]
    template = "BTOPage/bto_responsive_page_v2.html"

    def __str__(self):
        return self.caption


@register_snippet
class BTOPageInfoSnippet(BTOInfoSnippet):
    """ An PageInfoSnippet is a subclass of InfoSnippet, and presents a
        4-tuple of (image, caption, info, link_page).  
        It is typically used in CSS within an unordered list, 
        in a way that makes a responsive display of many PageInfoSnippets.
        The HOME page has many PageInfoSnippets for easy navigation to topic-pages.
    """

    link_page = models.ForeignKey(
        'wagtailcore.Page',
        null=False,
        blank=False,
        on_delete=models.CASCADE,
        related_name='+',
    )

    panels = BTOInfoSnippet.panels + [
        PageChooserPanel('link_page', 'BTOPage'),
    ]
    template = "BTOPage/bto_responsive_page_v2.html"

    def __str__(self):
        return self.caption


class BTOPage(Page):
    background_image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )

    author = models.CharField(
        max_length=64, default="William D. Torcaso", null=True, blank=True,
    )
    body = StreamField(
        [
            ("heading", CharBlock(classname="full title")),
            ("rtblock", RichTextBlock()),
            ("image", ImageChooserBlock()),
        ],
        null=True,
        blank=True,
    )
    info_stream = StreamField(
        [("info_snippet", SnippetChooserBlock(BTOInfoSnippet))], null=True, blank=True,
    )
    template = "BTOPage/bto_responsive_page_v2.html"

    content_panels = Page.content_panels + [
        ImageChooserPanel("background_image"),
        FieldPanel("author"),
        StreamFieldPanel("body"),
        StreamFieldPanel("info_stream"),
    ]
