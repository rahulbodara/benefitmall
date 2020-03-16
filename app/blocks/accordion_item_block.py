from wagtail.core.blocks import StructBlock, CharBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock


class AccordionItemBlock(StructBlock):
    title = CharBlock()
    body = RichTextBlock()

    class Meta:
        template = 'blocks/accordion_item_block.html'
        label = 'Item'
        icon = 'fa-map'
