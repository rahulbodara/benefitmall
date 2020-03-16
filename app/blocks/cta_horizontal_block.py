from wagtail.core.blocks import StructBlock, TextBlock

from app.choices import OUTLINE_CHOICES, SUBHEAD_SIZE_CHOICES, PARAGRAPH_SIZE_CHOICES
from app.widgets import CustomRadioSelect
from .custom_choice_block import CustomChoiceBlock
from .link_block import LinkBlock
from .background_block import BackgroundBlock


class CtaHorizontalBlock(StructBlock):
    header = TextBlock()
    subhead_size = CustomChoiceBlock(choices=SUBHEAD_SIZE_CHOICES, default=SUBHEAD_SIZE_CHOICES[1][0], required=False, widget=CustomRadioSelect, label='Size')
    body = TextBlock()
    body_size = CustomChoiceBlock(choices=PARAGRAPH_SIZE_CHOICES, default=PARAGRAPH_SIZE_CHOICES[1][0], required=False, widget=CustomRadioSelect, label='Body Size')
    outline = CustomChoiceBlock(choices=OUTLINE_CHOICES, required=False, widget=CustomRadioSelect, label='Outline')
    link = LinkBlock()
    background = BackgroundBlock()

    class Meta:
        icon = 'fa-bullhorn'
        template = 'blocks/cta_horizontal_block.html'
        label = 'CTA'
