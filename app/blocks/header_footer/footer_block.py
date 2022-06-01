from app.choices import LINK_TYPE_CHOICES, BUTTON_STYLE_CHOICES
from app.widgets import CustomRadioSelect
from app.blocks.custom_choice_block import CustomChoiceBlock
from app.blocks.link_block import LinkBlock
from app.blocks.category_link_block import CategoryLinkBlock



class GenericLinkBlock(LinkBlock):
    link_type = CustomChoiceBlock(label='Type', choices=LINK_TYPE_CHOICES[1:5], default=LINK_TYPE_CHOICES[1][0], required=False, widget=CustomRadioSelect)
    link_format = None


class FooterUtilityLinkBlock(GenericLinkBlock):

    class Meta:
        label = 'Link'
        icon = 'link'
        template = 'blocks/header_footer/footer_utility_link_block.html'


class FooterButtonBlock(GenericLinkBlock):
    button_style = CustomChoiceBlock(label='Style', choices=BUTTON_STYLE_CHOICES, default=BUTTON_STYLE_CHOICES[0][0], required=False, widget=CustomRadioSelect)

    class Meta:
        label = 'Button'
        icon = 'fa-square'
        template = 'blocks/header_footer/footer_button_block.html'


class FooterLinkBlock(GenericLinkBlock):

    class Meta:
        label = 'Link'
        icon = 'link'
        template = 'blocks/header_footer/footer_link_block.html'

class FooterCategoryBlock(CategoryLinkBlock):

    class Meta:

        label = 'Link'
        icon = 'link'
        template = 'blocks/header_footer/footer_category_link_block.html'