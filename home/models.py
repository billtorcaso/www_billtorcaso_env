from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField
from wagtail.core.fields import RichTextField
from wagtail.core import blocks

from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel

from wagtail.images.models import Image
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel


class HomePage(Page):
    background_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )
    author = models.CharField(max_length=64, default="William D. Torcaso")
    rtf_1 = RichTextField(blank=True)
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('rtf_2', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])


    content_panels = Page.content_panels + [
        ImageChooserPanel('background_image'),
        FieldPanel('author', classname="full"),
        FieldPanel('rtf_1', classname="full"),
        StreamFieldPanel('body', classname="full"),
    ]
