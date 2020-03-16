from django.utils.html import format_html
from wagtail.core.blocks import StructBlock, TextBlock
from wagtail.images.blocks import ImageChooserBlock

from app.choices import SWITCHABLE_CHOICES
from app.widgets import CustomRadioSelect
from .custom_choice_block import CustomChoiceBlock
from .multi_text_block import MultiTextBlock


class TabbedImagesItemBlock(StructBlock):
    image = ImageChooserBlock(required=True)
    icon = TextBlock(help_text=format_html('Choose an icon from the <a target="_blank" href="/admin/icon-reference">Icon Reference page</a>'))
    text = MultiTextBlock()
    layout = CustomChoiceBlock(choices=SWITCHABLE_CHOICES, default=SWITCHABLE_CHOICES[0][0], required=False, widget=CustomRadioSelect)
    
    class Meta:
        template = 'blocks/tabbed_images_item_block.html'
        label = 'Tabbed Image'
        icon = 'fa-photo'
