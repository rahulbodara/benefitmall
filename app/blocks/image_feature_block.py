from wagtail.core.blocks import StreamBlock, StructBlock, CharBlock

from app.choices import IMAGE_FEATURE_CHOICES, COLUMNS_BREAKPOINT_CHOICES, SUBHEAD_SIZE_CHOICES, IMAGE_OVERLAY_CHOICES, IMAGE_INVERT_CHOICES, PARAGRAPH_SIZE_CHOICES
from app.widgets import CustomRadioSelect
from .custom_choice_block import CustomChoiceBlock
from .image_feature_item_block import ImageFeatureItemBlock
from .background_block import BackgroundBlock


class ImageFeatureBlock(StructBlock):
    layout = CustomChoiceBlock(
        choices=IMAGE_FEATURE_CHOICES,
        default=IMAGE_FEATURE_CHOICES[0][0],
        required=True,
        widget=CustomRadioSelect
    )


    columns = CustomChoiceBlock(
        choices=COLUMNS_BREAKPOINT_CHOICES,
        default=COLUMNS_BREAKPOINT_CHOICES[0][0],
        required=True,
        widget=CustomRadioSelect
    )
    image_overlay = CustomChoiceBlock(choices=IMAGE_OVERLAY_CHOICES, default=IMAGE_OVERLAY_CHOICES[0][0],
                                      required=False, widget=CustomRadioSelect, label='Overlay Opacity')

    image_invert = CustomChoiceBlock(choices=IMAGE_INVERT_CHOICES, default=IMAGE_INVERT_CHOICES[0][0], required=False, widget=CustomRadioSelect, label='Invert Dark/Light')

    heading_size = CustomChoiceBlock(
        choices=SUBHEAD_SIZE_CHOICES,
        default=SUBHEAD_SIZE_CHOICES[0][0],
        required=False,
        widget=CustomRadioSelect, label='Heading Size'
    )
    body_size = CustomChoiceBlock(choices=PARAGRAPH_SIZE_CHOICES, default=PARAGRAPH_SIZE_CHOICES[1][0], required=False, widget=CustomRadioSelect, label='Body Size')

    items = StreamBlock([('imagefeatureitem', ImageFeatureItemBlock())], required=True)

    background = BackgroundBlock()

    class Meta:
        template = 'blocks/image_feature_block.html'
        label = 'Image Features'
        icon = 'fa-camera-retro'
        form_classname='image-feature-block struct-block'