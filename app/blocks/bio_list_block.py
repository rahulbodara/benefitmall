from wagtail.core.blocks import StreamBlock, StructBlock

from .bio_list_item_block import BioListItemBlock
from .background_block import BackgroundBlock
from app.choices.block_edit_choices import BIO_LAYOUT_CHOICES
from app.widgets import CustomRadioSelect
from .custom_choice_block import CustomChoiceBlock


class BioListBlock(StructBlock):
	layout = CustomChoiceBlock(choices=BIO_LAYOUT_CHOICES, default=BIO_LAYOUT_CHOICES[0][0], required=True, widget=CustomRadioSelect)
	bios = StreamBlock([('biolistitem', BioListItemBlock())], label='Bios', required=True)
	background = BackgroundBlock()

	class Meta:
		icon = 'fa-users'
		template = 'blocks/bio_list_block.html'
		label = 'Bio List'
