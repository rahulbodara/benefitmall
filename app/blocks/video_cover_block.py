from wagtail.core.blocks import StructBlock, URLBlock, CharBlock, BooleanBlock, TextBlock
from wagtail.images.blocks import ImageChooserBlock

from .multi_text_block import MultiTextBlock
from .background_block import BackgroundBlock
from .link_block import LinkBlock

class VideoCoverBlock(StructBlock):
    video_id = CharBlock(required=True, help_text="Youtube Video ID")
    autoplay = BooleanBlock(required=False)
    placeholder_image = ImageChooserBlock(required=True)
    title = CharBlock(required=False)
    text = TextBlock(required=False)
    link = LinkBlock()

    class Meta:
        template = 'blocks/video_cover_block.html'
        icon = 'fa-play'
        label = 'Video Cover'
