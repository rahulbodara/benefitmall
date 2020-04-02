from wagtail.core.blocks import StructBlock, TextBlock, PageChooserBlock

from app.choices import OUTLINE_CHOICES, SUBHEAD_SIZE_CHOICES, PARAGRAPH_SIZE_CHOICES, CTA_LAYOUT_CHOICES
from app.widgets import CustomRadioSelect
from .custom_choice_block import CustomChoiceBlock
from .link_block import LinkBlock
from .background_block import BackgroundBlock


class CtaHorizontalBlock(StructBlock):
    layout = CustomChoiceBlock(choices=CTA_LAYOUT_CHOICES, default=CTA_LAYOUT_CHOICES[1][0], required=True, widget=CustomRadioSelect, label='Layout')
    header = TextBlock()
    subhead_size = CustomChoiceBlock(choices=SUBHEAD_SIZE_CHOICES, default=SUBHEAD_SIZE_CHOICES[1][0], required=False, widget=CustomRadioSelect, label='Header Size')
    body = TextBlock(required=False, label='Body')
    body_size = CustomChoiceBlock(choices=PARAGRAPH_SIZE_CHOICES, default=PARAGRAPH_SIZE_CHOICES[1][0], required=False, widget=CustomRadioSelect, label='Body Size')
    outline = CustomChoiceBlock(choices=OUTLINE_CHOICES, default=OUTLINE_CHOICES[1][0], required=False, widget=CustomRadioSelect, label='Outline')
    page = PageChooserBlock(required=False, label='Link')
    link = LinkBlock()
    background = BackgroundBlock()

    class Meta:
        icon = 'fa-bullhorn'
        template = 'blocks/cta_block.html'
        label = 'CTA'
        form_classname = 'cta-block struct-block'
