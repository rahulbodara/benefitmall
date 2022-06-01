from django.forms.utils import ErrorList

from wagtail.core.blocks import CharBlock, BooleanBlock, StructValue, StructBlock, StreamBlock, StreamBlockValidationError
from wagtail.images.blocks import ImageChooserBlock

from app.widgets import CustomRadioSelect
from app.blocks.custom_choice_block import CustomChoiceBlock
from app.blocks.link_block import LinkBlock


class SubLinkBlock(StreamBlock):
    link = LinkBlock()

class GroupLinkBlock(StructBlock):
    top = LinkBlock(label='Parent')
    sub = SubLinkBlock(label='Children')
    show_children = BooleanBlock()

class ParentLinkBlock(StreamBlock):
    parent = GroupLinkBlock(label='Parent')
    #sub = SubLinkBlock(label='Children')
    # show_children = BooleanBlock()

class ButtonBlock(StreamBlock):
    thing = CharBlock()

class NavStandardBarBlock(StructBlock):
    links = ParentLinkBlock(label='Links')
    buttons = ButtonBlock()

class NavCenteredBarBlock(StructBlock):
    thing = CharBlock()

class NavAppBarBlock(StructBlock):
    thing = CharBlock()

class NavFullscreenBlock(StructBlock):
    thing = CharBlock()

class NavSidebarBlock(StructBlock):
    thing = CharBlock()

class NavBlock(StreamBlock):
    standard_bar = NavStandardBarBlock()
    centered_bar = NavCenteredBarBlock()
    app_bar = NavAppBarBlock()
    fullscreen = NavFullscreenBlock()
    sidebar = NavSidebarBlock()

class HeaderBlock(StructBlock):
    NAV_SKIN_CHOICES = (
        ('', 'Light'),
        ('', 'Dark'),
    )
    NAV_BACKGROUND_CHOICES = (
        ('', 'Solid'),
        ('', 'Transparent'),
    )
    nav = NavBlock()
    skin = CustomChoiceBlock(choices=NAV_SKIN_CHOICES, default=NAV_SKIN_CHOICES[0][0], required=False, widget=CustomRadioSelect)
    background = CustomChoiceBlock(choices=NAV_BACKGROUND_CHOICES, default=NAV_BACKGROUND_CHOICES[0][0], required=False, widget=CustomRadioSelect)

    class Meta:
        template = 'blocks/settings/header_block.html'
        label = 'Header'
        #form_classname = 'header-block struct-block'
        #value_class = BackgroundBlockStructValue
