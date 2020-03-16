from django import forms
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.blocks import StructBlock, TextBlock, RichTextBlock, ChoiceBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel


class iFrameBlock(StructBlock):

    src = TextBlock(help_text='The URL the iFrame should point to.')
    name = TextBlock(help_text='The name of the iFrame element.')
    width = TextBlock(default='100%', help_text='The width of the iFrame (default is 100%).')
    height = TextBlock(default='600px', help_text='The height of the iFrame (default is 600px).')
    frameborder = TextBlock(default='0', help_text='The width of the iFrame border (default is 0).')

    class Meta:
        template = 'blocks/iframe.html'
        label = 'Embedded iFrame'
        icon = 'fa-square'
