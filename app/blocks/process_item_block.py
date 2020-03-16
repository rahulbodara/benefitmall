from wagtail.core.blocks import CharBlock, StructBlock, TextBlock
from wagtail.images.blocks import ImageChooserBlock

from .link_block import LinkBlock


class ProcessItemBlock(StructBlock):
    title = CharBlock()
    text = TextBlock()
    # image = ImageChooserBlock()
    # link = LinkBlock()

    class Meta:
        template = 'blocks/process_item_block.html'
        label = 'Process/Timeline Item'
        icon = 'fa-braille'
