from wagtail.core.blocks import StructBlock

from .multi_text_block import MultiTextBlock
from .background_block import BackgroundBlock


class TitleBlock(StructBlock):
    text = MultiTextBlock()
    background = BackgroundBlock()

    class Meta:
        template = 'blocks/title_block.html'
        icon = 'fa-align-center'
        label = 'Title'
