from wagtail.core.blocks import StructBlock, CharBlock

from app.widgets import CustomRadioSelect
from .custom_choice_block import CustomChoiceBlock
from app.choices import SWITCHABLE_CHOICES, WIDTH_CHOICES
from .multi_text_block import MultiTextBlock
from .background_block import BackgroundBlock


class TitleBlock(StructBlock):
    layout = CustomChoiceBlock(choices=WIDTH_CHOICES, default=WIDTH_CHOICES[1][0], widget=CustomRadioSelect, label='Layout')
    switchable = CustomChoiceBlock(choices=SWITCHABLE_CHOICES, default=SWITCHABLE_CHOICES[0][0], widget=CustomRadioSelect)
    text = MultiTextBlock()
    background = BackgroundBlock()

    class Meta:
        template = 'blocks/title_block.html'
        icon = 'fa-align-center'
        label = 'Title'
