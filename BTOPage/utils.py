from django.db import models


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


@register_snippet
class Advert(models.Model):
    """
    At the moment, this is junk brought in for debugging.
    """
    url = models.URLField(null=True, blank=True)
    text = models.CharField(max_length=255)

    panels = [
        FieldPanel('url'),
        FieldPanel('text'),
    ]

    def __str__(self):
        return self.text


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
