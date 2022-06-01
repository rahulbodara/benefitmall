from wagtail.core.blocks import CharBlock, StructBlock, TextBlock
from wagtail.images.blocks import ImageChooserBlock


class ImageSliderItemBlock(StructBlock):
    image = ImageChooserBlock()

    class Meta:
        template = 'blocks/image_slider_item_block.html'
        label = 'Slider Image'
        icon = 'fa-columns'
