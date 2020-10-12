from wagtail.core.blocks import StreamBlock, StructBlock, CharBlock, RichTextBlock

from app.choices import IMAGE_FEATURE_CHOICES, COLUMNS_BREAKPOINT_CHOICES_5, SUBHEAD_SIZE_CHOICES, IMAGE_OVERLAY_CHOICES, IMAGE_INVERT_CHOICES, PARAGRAPH_SIZE_CHOICES, HORIZONTAL_ALIGNMENT_CHOICES, HEADING_SIZE_CHOICES
from app.widgets import CustomRadioSelect
from .custom_choice_block import CustomChoiceBlock
from .image_feature_item_block import ImageFeatureItemBlock
from .background_block import BackgroundBlock
from .multi_text_block import MultiTextBlock


class ImageFeatureBlock(StructBlock):
    title_alignment = CustomChoiceBlock(choices=HORIZONTAL_ALIGNMENT_CHOICES, default=HORIZONTAL_ALIGNMENT_CHOICES[0][0], required=False, widget=CustomRadioSelect, label='Title Alignment')
    title_heading = CharBlock(required=False, label='Title')
    title_heading_size = CustomChoiceBlock(choices=HEADING_SIZE_CHOICES, default=HEADING_SIZE_CHOICES[0][0], required=False, widget=CustomRadioSelect, label='Title Size')
    title_body = RichTextBlock(required=False, features=['h3', 'h4', 'h5', 'bold', 'italic', 'ol', 'ul', 'link', 'document-link'], label='Into Body')
    title_body_size = CustomChoiceBlock(choices=PARAGRAPH_SIZE_CHOICES, default=PARAGRAPH_SIZE_CHOICES[1][0], required=False, widget=CustomRadioSelect, label='Intro Body Size')
    layout = CustomChoiceBlock(
        choices=IMAGE_FEATURE_CHOICES,
        default=IMAGE_FEATURE_CHOICES[0][0],
        required=True,
        widget=CustomRadioSelect
    )


    columns = CustomChoiceBlock(
        choices=COLUMNS_BREAKPOINT_CHOICES_5,
        default=COLUMNS_BREAKPOINT_CHOICES_5[0][0],
        required=True,
        widget=CustomRadioSelect
    )
    item_image_overlay = CustomChoiceBlock(choices=IMAGE_OVERLAY_CHOICES, default=IMAGE_OVERLAY_CHOICES[0][0],
                                      required=False, widget=CustomRadioSelect, label='Overlay Opacity')

    item_image_invert = CustomChoiceBlock(choices=IMAGE_INVERT_CHOICES, default=IMAGE_INVERT_CHOICES[0][0], required=False, widget=CustomRadioSelect, label='Invert Dark/Light')

    item_alignment = CustomChoiceBlock(choices=HORIZONTAL_ALIGNMENT_CHOICES, default=HORIZONTAL_ALIGNMENT_CHOICES[0][0], required=False, widget=CustomRadioSelect, label='Item Alignment')

    heading_size = CustomChoiceBlock(
        choices=SUBHEAD_SIZE_CHOICES,
        default=SUBHEAD_SIZE_CHOICES[0][0],
        required=False,
        widget=CustomRadioSelect, label='Item Heading Size'
    )
    body_size = CustomChoiceBlock(choices=PARAGRAPH_SIZE_CHOICES, default=PARAGRAPH_SIZE_CHOICES[1][0], required=False, widget=CustomRadioSelect, label='Item Body Size')

    items = StreamBlock([('imagefeatureitem', ImageFeatureItemBlock())], required=True)

    background = BackgroundBlock()

    class Meta:
        template = 'blocks/image_feature_block.html'
        label = 'Image Features'
        icon = 'fa-camera-retro'
        form_classname='image-feature-block struct-block'