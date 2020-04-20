from django.utils.html import format_html

from wagtail.core.blocks import CharBlock, TextBlock, StructBlock, RichTextBlock
from .link_block import LinkBlock


class IconFeatureItemBlock(StructBlock):
    header = CharBlock()
    text = RichTextBlock(required=False)
    icon = CharBlock(help_text=format_html('Choose an icon from the <a target="_blank" href="/admin/icon-reference/">Icon Reference page</a>'))
    link = LinkBlock()

    class Meta:
        template = 'blocks/icon_feature_item_block.html'
        label = 'Icon Feature'
        icon = 'fa-info-circle'
