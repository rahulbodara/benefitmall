from django import forms
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.blocks import StructBlock, TextBlock, RichTextBlock, ChoiceBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel


class AnchorBlock(StructBlock):

    name = TextBlock(help_text='The name of the anchor for linking to.')

    class Meta:
        template = 'blocks/anchor.html'
        label = 'Anchor'
        icon = 'fa-anchor'
