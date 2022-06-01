from wagtail.core.blocks import StreamBlock, StructBlock

from .tabbed_images_item_block import TabbedImagesItemBlock
from .background_block import BackgroundBlock


class TabbedImagesBlock(StructBlock):
	items = StreamBlock([('tabbedimageitem', TabbedImagesItemBlock())], required=True)
	background = BackgroundBlock()

	class Meta:
		template = 'blocks/tabbed_images_block.html'
		label = 'Tabbed Images'
		icon = 'fa-photo'
