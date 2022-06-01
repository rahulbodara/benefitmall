from wagtail.core.blocks import StreamBlock, StructBlock

from .testimonial_item_block import TestimonialItemBlock
from .background_block import BackgroundBlock


class TestimonialBlock(StructBlock):
	items = StreamBlock([('testimonialitem', TestimonialItemBlock())], required=True)
	background = BackgroundBlock()
	
	class Meta:
		template = 'blocks/testimonial_block.html'
		label = 'Testimonial List'
		icon = 'fa-book'
