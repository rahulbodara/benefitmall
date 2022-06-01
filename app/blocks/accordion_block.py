from wagtail.core.blocks import StreamBlock, StructBlock

from .accordion_item_block import AccordionItemBlock
from .custom_choice_block import CustomChoiceBlock
from app.widgets import CustomRadioSelect
from .background_block import BackgroundBlock
from app.choices import HORIZONTAL_ALIGNMENT_CHOICES, ACCORDION_FORMAT_CHOICES, ACCORDION_OPEN_DEFAULTCHOICES

class AccordionBlock(StructBlock):
    style = CustomChoiceBlock(
        choices=ACCORDION_FORMAT_CHOICES,
        default=ACCORDION_FORMAT_CHOICES[0][0],
        required=True,
        widget=CustomRadioSelect,
    )
    alignment = CustomChoiceBlock(
        choices=HORIZONTAL_ALIGNMENT_CHOICES,
        default=HORIZONTAL_ALIGNMENT_CHOICES[0][0],
        required=False,
        widget=CustomRadioSelect,
    )
    default_active = CustomChoiceBlock(
        choices=ACCORDION_OPEN_DEFAULTCHOICES,
        default=ACCORDION_OPEN_DEFAULTCHOICES[0][0],
        required=False,
        widget=CustomRadioSelect,
        label='Open First By Default?',
    )
    items = StreamBlock(
        [('accordionitem', AccordionItemBlock())],
        label='Items',
        required=True,
    )
    background = BackgroundBlock()

    class Meta:
        icon = 'fa-map'
        template = 'blocks/accordion_block.html'
        label = 'Accordion'
