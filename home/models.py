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

class SegmentBlock(blocks.StructBlock):
    extra_klasses = blocks.CharBlock(required=False, help_text='semantic ui classes (eg: raised ...')
    name = blocks.CharBlock(required=False, help_text='sets an anchor text id. Can leave blank')
    header = blocks.RichTextBlock(required=False, help_text='Can leave blank')
    content = blocks.RichTextBlock(required=False, help_text='template tags are available eg: {{ user }} ,'
                                             ' {{ last_login }}, {{ now }}, {{ today }} {{request }}')
    divider = blocks.BooleanBlock(required=False)
    boxed = blocks.BooleanBlock(required=False)
    published = blocks.BooleanBlock(required=False, default=True)


    class Meta:
        icon = 'user'
        label = 'Segment'
        admin_text = 'Segment'
        template = 'cms/blocks/segment.html'

    def get_context(self, value, parent_context=None):
        context = super(SegmentBlock, self).get_context(value, parent_context=parent_context)
        context['today'] = datetime.date.today()
        context['now'] = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        context_value = context.get('value', {})
        template_text = context_value.get('content', 'No content').source
        t = Template(template_text)
        content_context = {
            "user": context['request'].user,
            "last_login": context['request'].user.last_login.strftime('%Y-%m-%d %H:%M:%S'),
            "now": context['now'],
            "today": context['today'],
            "request": context['request'],
        }
        context['content'] = t.render(Context(content_context))
        return context


class ColumnBlock(blocks.StreamBlock):
    heading = blocks.CharBlock(classname="full title")
    paragraph = blocks.RichTextBlock()
    image = ImageChooserBlock()
    segment = SegmentBlock()

    class Meta:
        template = 'cms/blocks/column.html'


class TwoColumnBlock(blocks.StructBlock):
    DEFAULT_TEMPLATE_LAYOUT = 'cms/blocks/even_column_block.html'
    TEMPLATE_CHOICES = [
        (DEFAULT_TEMPLATE_LAYOUT, '2 even Col'),
        ('cms/blocks/big_right_column_block.html', 'Big right'),
        ('cms/blocks/big_left_column_block.html', 'Big left')
    ]

    left_column = ColumnBlock(icon='arrow-right', label='Left column content')
    right_column = ColumnBlock(icon='arrow-right', label='Right column content')
    boxed = blocks.BooleanBlock(required=False)
    extra_klasses = blocks.CharBlock(required=False, help_text='semantic ui classes (eg: raised ...')
    template = blocks.ChoiceBlock(choices=TEMPLATE_CHOICES, default=DEFAULT_TEMPLATE_LAYOUT)

    class Meta:
        template = 'cms/blocks/two_column_block.html'
        icon = 'placeholder'
        label = 'Two Columns'


class HomePage(Page):
    # see templates/cms/general_page.html
    # note special handling of 'header' content type in template file
    body = StreamField([
        ('segment', SegmentBlock(classname="segment")),
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock(icon="image")),
        ('two_columns', TwoColumnBlock()),
        ('embedded_video', EmbedBlock(icon="media")),
    ], null=True, blank=True)

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]
