from django import forms
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from wagtail.core.blocks import StructBlock, TextBlock, RichTextBlock, ChoiceBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.edit_handlers import ImageChooserPanel


class SitemapBlock(StructBlock):

    class Meta:
        template = 'blocks/sitemap.html'
        label = 'Site Map'
        icon = 'fa-map'
