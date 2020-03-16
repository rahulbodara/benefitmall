from wagtail.core.blocks import StreamBlock, StructBlock

from app.choices import IMAGE_FEATURE_CHOICES
from app.widgets import CustomRadioSelect
from .custom_choice_block import CustomChoiceBlock
from .image_feature_item_block import ImageFeatureItemBlock
from .background_block import BackgroundBlock


class ImageFeatureBlock(StructBlock):
    layout = CustomChoiceBlock(choices=IMAGE_FEATURE_CHOICES, default=IMAGE_FEATURE_CHOICES[0][0], required=True, widget=CustomRadioSelect)
    items = StreamBlock([('imagefeatureitem', ImageFeatureItemBlock())], required=True)
    background = BackgroundBlock()
    
    class Meta:
        template = 'blocks/image_feature_block.html'
        label = 'Image Features'
        icon = 'fa-camera-retro'
