from wagtail.core.blocks import StreamBlock, StructBlock
from wagtail.images.blocks import ImageChooserBlock

from app.choices import ICON_FEATURE_CHOICES
from app.widgets import CustomRadioSelect
from .background_block import BackgroundBlock
from .custom_choice_block import CustomChoiceBlock
from .icon_feature_item_block import IconFeatureItemBlock


class IconFeatureBlock(StructBlock):
    layout = CustomChoiceBlock(choices=ICON_FEATURE_CHOICES, default=ICON_FEATURE_CHOICES[0][0], required=True, widget=CustomRadioSelect)
    items = StreamBlock([('iconfeatureitem', IconFeatureItemBlock())], required=True)
    background = BackgroundBlock()

    class Meta:
        template = 'blocks/icon_feature_block.html'
        label = 'Icon Features'
        icon = 'fa-info-circle'
