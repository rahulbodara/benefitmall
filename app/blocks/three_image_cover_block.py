from django.forms.utils import ErrorList

from wagtail.core.blocks import StructValue, StructBlock, StreamBlockValidationError, CharBlock, TextBlock
from wagtail.images.blocks import ImageChooserBlock

from app.blocks.background_block import BackgroundBlock
from app.blocks.link_block import LinkBlock
from app.widgets import CustomRadioSelect
from app.choices import IMAGE_MODE_CHOICES, IMAGE_EFFECT_CHOICES, IMAGE_INVERT_CHOICES, IMAGE_OVERLAY_CHOICES, PADDING_CHOICES, BACKGROUND_SIZE_CHOICES, BACKGROUND_SIZING_MODE
from .custom_choice_block import CustomChoiceBlock


class ThreeImageCoverBlock(StructBlock):
    title = CharBlock(required=False)
    text = TextBlock(required=False)
    link = LinkBlock()
    image_left = ImageChooserBlock(required=False)
    image_center = ImageChooserBlock(required=False)
    image_right = ImageChooserBlock(required=False)
    background = BackgroundBlock()

    class Meta:
        template = 'blocks/three_image_cover_block.html'
        label = 'Three Image Cover Block'
        icon = 'fa-square-o'
