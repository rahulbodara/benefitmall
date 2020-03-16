from django.forms.utils import ErrorList

from wagtail.core.blocks import StructValue, StructBlock, StreamBlockValidationError
from wagtail.images.blocks import ImageChooserBlock

from app.widgets import CustomRadioSelect
from app.choices import IMAGE_MODE_CHOICES, IMAGE_EFFECT_CHOICES, IMAGE_INVERT_CHOICES, IMAGE_OVERLAY_CHOICES, PADDING_CHOICES, BACKGROUND_SIZE_CHOICES, BACKGROUND_SIZING_MODE
from .custom_choice_block import CustomChoiceBlock


class ImageBlock(StructBlock):
    mode = CustomChoiceBlock(choices=IMAGE_MODE_CHOICES, default=IMAGE_MODE_CHOICES[0][0], required=False, widget=CustomRadioSelect)
    image = ImageChooserBlock(required=False)
    image_effect = CustomChoiceBlock(choices=IMAGE_EFFECT_CHOICES, default=IMAGE_EFFECT_CHOICES[0][0], required=False, widget=CustomRadioSelect, label='Image Effect')
    image_invert = CustomChoiceBlock(choices=IMAGE_INVERT_CHOICES, default=IMAGE_INVERT_CHOICES[0][0], required=False, widget=CustomRadioSelect, label='Invert Dark/Light')
    image_overlay = CustomChoiceBlock(choices=IMAGE_OVERLAY_CHOICES, default='4', required=False, widget=CustomRadioSelect, label='Overlay Opacity')
    sizing_mode = CustomChoiceBlock(choices=BACKGROUND_SIZING_MODE, default=BACKGROUND_SIZING_MODE[0][0], required=False, widget=CustomRadioSelect)
    padding = CustomChoiceBlock(choices=PADDING_CHOICES, default=PADDING_CHOICES[3][0], required=False, widget=CustomRadioSelect)
    sizing = CustomChoiceBlock(choices=BACKGROUND_SIZE_CHOICES, default=BACKGROUND_SIZE_CHOICES[4][0], required=False, widget=CustomRadioSelect)

    class Meta:
        template = 'blocks/image_block.html'
        label = 'Image Block'
        icon = 'image'
