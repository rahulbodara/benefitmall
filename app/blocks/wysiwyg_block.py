from wagtail.core.blocks import StructBlock, RichTextBlock

from app.widgets import CustomRadioSelect
from app.choices import HORIZONTAL_ALIGNMENT_CHOICES, PARAGRAPH_SIZE_CHOICES, PADDING_CHOICES
from .custom_choice_block import CustomChoiceBlock


class WYSIWYGBlock(StructBlock):
    alignment = CustomChoiceBlock(choices=HORIZONTAL_ALIGNMENT_CHOICES, default=HORIZONTAL_ALIGNMENT_CHOICES[0][0], required=False, widget=CustomRadioSelect)
    body = RichTextBlock(required=False)
    body_size = CustomChoiceBlock(choices=PARAGRAPH_SIZE_CHOICES, default=PARAGRAPH_SIZE_CHOICES[1][0], required=False, widget=CustomRadioSelect, label='Size')
    padding = CustomChoiceBlock(choices=PADDING_CHOICES, default=PADDING_CHOICES[3][0], required=False, widget=CustomRadioSelect)

    class Meta:
        template = 'blocks/wysiwyg_block.html'
        icon = 'pilcrow'
        label = 'WYSIWYG'
