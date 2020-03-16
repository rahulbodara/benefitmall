from wagtail.core.blocks import StructBlock, StreamBlock

from app.choices import LINK_TYPE_CHOICES, BUTTON_STYLE_CHOICES
from app.widgets import CustomRadioSelect
from app.blocks.custom_choice_block import CustomChoiceBlock
from app.blocks.link_block import LinkBlock


class GenericLinkBlock(LinkBlock):
    link_type = CustomChoiceBlock(label='Type', choices=LINK_TYPE_CHOICES[1:5], default=LINK_TYPE_CHOICES[1][0], required=False, widget=CustomRadioSelect)
    link_format = None

    class Meta:
        template = 'blocks/header_footer/header_link_block.html'


class HeaderButtonBlock(GenericLinkBlock):
    button_style = CustomChoiceBlock(label='Style', choices=BUTTON_STYLE_CHOICES, default=BUTTON_STYLE_CHOICES[0][0], required=False, widget=CustomRadioSelect)

    class Meta:
        label = 'Button'
        icon = 'fa-square'
        template = 'blocks/header_footer/header_button_block.html'


class ChildLinkBlock(StreamBlock):
    link = GenericLinkBlock()

    class Meta:
        label = 'Child'


class ParentLinkBlock(GenericLinkBlock):
    children = ChildLinkBlock(null=True, blank=True, required=False)

    class Meta:
        label = 'Parent'


class HeaderLinkBlock(StructBlock):
    link = ParentLinkBlock()

    class Meta:
        label = 'Link'
        icon = 'link'
