from wagtail.core.blocks import StructBlock, CharBlock, TextBlock, RichTextBlock

from app.widgets import CustomRadioSelect
from app.choices import HORIZONTAL_ALIGNMENT_CHOICES, SUBHEAD_SIZE_CHOICES
from .custom_choice_block import CustomChoiceBlock


class ThreeColumnItemBlock(StructBlock):
    header = CharBlock()
    subhead_size = CustomChoiceBlock(choices=SUBHEAD_SIZE_CHOICES, default=SUBHEAD_SIZE_CHOICES[1][0], required=False, widget=CustomRadioSelect, label='Size')

    text = RichTextBlock(features=['bold', 'italic', 'ol', 'ul', 'link', 'document-link'])
    alignment = CustomChoiceBlock(choices=HORIZONTAL_ALIGNMENT_CHOICES, default=HORIZONTAL_ALIGNMENT_CHOICES[0][0], required=False, widget=CustomRadioSelect)

    class Meta:
        template = 'blocks/three_column_item_block.html'
        label = 'Column'
        icon = 'placeholder'
