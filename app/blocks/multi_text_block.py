from wagtail.core.blocks import CharBlock, TextBlock, RichTextBlock, StructValue, StructBlock

from app.widgets import CustomRadioSelect
from app.choices import HORIZONTAL_ALIGNMENT_CHOICES, HEADING_SIZE_CHOICES, PARAGRAPH_SIZE_CHOICES
from .custom_choice_block import CustomChoiceBlock
from .link_block import LinkBlock


class MultiTextBlock(StructBlock):
    alignment = CustomChoiceBlock(choices=HORIZONTAL_ALIGNMENT_CHOICES, default=HORIZONTAL_ALIGNMENT_CHOICES[0][0], required=False, widget=CustomRadioSelect)
    heading = CharBlock()
    heading_size = CustomChoiceBlock(choices=HEADING_SIZE_CHOICES, default=HEADING_SIZE_CHOICES[0][0], required=False, widget=CustomRadioSelect, label='Heading Size')
    body = RichTextBlock(required=False, features=['h3', 'h4', 'h5', 'bold', 'italic', 'ol', 'ul', 'link', 'document-link'])
    body_size = CustomChoiceBlock(choices=PARAGRAPH_SIZE_CHOICES, default=PARAGRAPH_SIZE_CHOICES[1][0], required=False, widget=CustomRadioSelect, label='Body Size')
    link = LinkBlock()
    caption = TextBlock(required=False)

    class Meta:
        template = 'blocks/multi_text_block.html'
        form_classname = 'multi-text-block struct-block'
