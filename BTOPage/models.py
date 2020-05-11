from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core import blocks

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from wagtail.images.models import Image
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel



class BTOPage(Page):
    background_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    author = models.CharField(max_length=64, default="William D. Torcaso")
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        ImageChooserPanel('background_image'),
        FieldPanel('author'),
        StreamFieldPanel('body'),
    ]
