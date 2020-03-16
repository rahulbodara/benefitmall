from wagtail.core.blocks import StructBlock, StructValue

from app.choices import SWITCHABLE_CHOICES, VERTICAL_ALIGNMENT_CHOICES, WIDTH_CHOICES
from app.widgets import CustomRadioSelect
from .custom_choice_block import CustomChoiceBlock
from .background_block import BackgroundBlock
from .media_block import MediaBlock
from .multi_text_block import MultiTextBlock


class MediaTitleBlock(StructBlock):
    width = CustomChoiceBlock(choices=WIDTH_CHOICES, default=WIDTH_CHOICES[0][0], required=False, widget=CustomRadioSelect)
    layout = CustomChoiceBlock(choices=SWITCHABLE_CHOICES, default=SWITCHABLE_CHOICES[0][0], required=False, widget=CustomRadioSelect)
    media = MediaBlock()    
    vertical_alignment = CustomChoiceBlock(choices=VERTICAL_ALIGNMENT_CHOICES, default=VERTICAL_ALIGNMENT_CHOICES[0][0], required=False, widget=CustomRadioSelect, label='Vertical Alignment')
    text = MultiTextBlock()
    background = BackgroundBlock()

    class Meta:
        icon = 'fa-id-card'
        template = 'blocks/media_title_block.html'
        label = 'Media + Title'
