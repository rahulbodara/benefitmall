from wagtail.core.blocks import CharBlock, StructBlock, TextBlock
from wagtail.images.blocks import ImageChooserBlock

from .link_block import LinkBlock


class ImageFeatureItemBlock(StructBlock):
    header = CharBlock()
    text = TextBlock(required=False)
    image = ImageChooserBlock()
    link = LinkBlock()

    class Meta:
        template = 'blocks/image_feature_item_block.html'
        label = 'Image Feature'
        icon = 'fa-camera-retro'
