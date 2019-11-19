from django.db import models
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.core.fields import RichTextField

from wagtail.core.models import Page
from wagtail.core import blocks
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.edit_handlers import (FieldPanel, FieldRowPanel,
                                         InlinePanel, MultiFieldPanel,
                                         PageChooserPanel, StreamFieldPanel)
from wagtail.core import blocks
from wagtail.core.fields import StreamField
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
import datetime
from django.template import Template, Context

from wagtail.core.models import Page

class ButtonBlock(blocks.StructBlock):
    label = blocks.CharBlock(required=False, help_text='button label')
    klass = blocks.CharBlock(required=False, help_text='button colour')
    url = blocks.URLBlock(icon='arrow-right', required=False)

    class Meta:
        template = 'home/blocks/button_block.html'
        icon = 'button'
        label = 'Button'


class SegmentBlock(blocks.StructBlock):
    extra_klasses = blocks.CharBlock(required=False, help_text='semantic ui classes (eg: raised ...')
    header = blocks.RichTextBlock(required=False, help_text='Can leave blank')
    content = blocks.RichTextBlock(required=False, help_text='template tags are available eg: {{ user }} ,'
                                             ' {{ last_login }}, {{ now }}, {{ today }} {{request }}')
    divider = blocks.BooleanBlock(required=False)
    boxed = blocks.BooleanBlock(required=False)

    class Meta:
        icon = 'user'
        label = 'Segment'
        admin_text = 'Segment'
        template = 'home/blocks/segment.html'


class ColumnBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(classname="full title")
    image = ImageChooserBlock()
    segment = SegmentBlock()
    embedded_video = EmbedBlock(icon="media")
    button = ButtonBlock(icon='button')

    class Meta:
        template = 'home/blocks/column.html'


class TwoColumnBlock(blocks.StructBlock):
    left_column = ColumnBlock(icon='arrow-right', label='Left column content')
    right_column = ColumnBlock(icon='arrow-right', label='Right column content')
    boxed = blocks.BooleanBlock(required=False)
    extra_klasses = blocks.CharBlock(required=False)

    class Meta:
        template = 'home/blocks/two_column_block.html'
        icon = 'placeholder'
        label = 'Two Columns'



class HomePage(Page):
    body = StreamField([
        ('segment', SegmentBlock(classname="segment")),
        ('heading', blocks.CharBlock(classname="full title")),
        ('image', ImageChooserBlock(icon="image")),
        ('two_columns', TwoColumnBlock()),
        ('embedded_video', EmbedBlock(icon="media")),
        ('button', ButtonBlock(icon="button")),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
