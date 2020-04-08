from wagtail.core.blocks import StreamBlock, StructBlock

from app.choices import IMAGE_SLIDER_ARROW_CHOICES, IMAGE_SLIDER_CHOICES, IMAGE_SLIDER_PAGING_CHOICES, IMAGE_SLIDER_SPEED_CHOICES
from app.widgets import CustomRadioSelect
from .custom_choice_block import CustomChoiceBlock
from .image_slider_item_block import ImageSliderItemBlock
from .background_block import BackgroundBlock


class ImageSliderBlock(StructBlock):
    slider_size = CustomChoiceBlock(choices=IMAGE_SLIDER_CHOICES, required=True,
                               widget=CustomRadioSelect)
    arrows = CustomChoiceBlock(choices=IMAGE_SLIDER_ARROW_CHOICES, default=IMAGE_SLIDER_ARROW_CHOICES[0][0], widget=CustomRadioSelect, label='Page Arrows')
    paging = CustomChoiceBlock(choices=IMAGE_SLIDER_PAGING_CHOICES, default=IMAGE_SLIDER_PAGING_CHOICES[0][0], widget=CustomRadioSelect, label='Page Bubbles')
    speed = CustomChoiceBlock(choices=IMAGE_SLIDER_SPEED_CHOICES, default=IMAGE_SLIDER_SPEED_CHOICES[0][0], widget=CustomRadioSelect, label='Slider Speed')
    items = StreamBlock([('sliderimage', ImageSliderItemBlock())], required=True)
    background = BackgroundBlock()

    class Meta:
        template = 'blocks/image_slider_block.html'
        label = 'Image Slider'
        icon = 'fa-columns'
