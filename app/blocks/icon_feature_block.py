from wagtail.core.blocks import StreamBlock, StructBlock
from wagtail.images.blocks import ImageChooserBlock

from app.choices import COLUMNS_BREAKPOINT_CHOICES
from app.widgets import CustomRadioSelect
from .background_block import BackgroundBlock
from .custom_choice_block import CustomChoiceBlock
from .icon_feature_item_block import IconFeatureItemBlock


class IconFeatureBlock(StructBlock):
    columns = CustomChoiceBlock(
        choices=COLUMNS_BREAKPOINT_CHOICES,
        default=COLUMNS_BREAKPOINT_CHOICES[0][0],
        required=True,
        widget=CustomRadioSelect
    )
    items = StreamBlock([('iconfeatureitem', IconFeatureItemBlock())], required=True)
    background = BackgroundBlock()

    class Meta:
        template = 'blocks/icon_feature_block.html'
        label = 'Icon Features'
        icon = 'fa-info-circle'
