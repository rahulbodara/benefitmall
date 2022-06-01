from wagtail.core.blocks import StreamBlock, StructBlock

from .three_column_item_block import ThreeColumnItemBlock
from .background_block import BackgroundBlock


class ThreeColumnBlock(StructBlock):
	items = StreamBlock([('columnlistitem', ThreeColumnItemBlock())], required=True)
	background = BackgroundBlock()

	class Meta:
		template = 'blocks/three_column_block.html'
		label = 'Three Column'
		icon = 'table'
