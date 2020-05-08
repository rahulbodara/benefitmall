from wagtail.core.blocks import StructBlock

from app.choices.block_edit_choices import MAX_ITEMS_CHOICES
from app.widgets import CustomRadioSelect

from .background_block import BackgroundBlock
from .custom_choice_block import CustomChoiceBlock


class RecentNewsBlock(StructBlock):
	max_items = CustomChoiceBlock(label='Max Items', choices=MAX_ITEMS_CHOICES, default=MAX_ITEMS_CHOICES[0][0], required=False, widget=CustomRadioSelect)
	background = BackgroundBlock()

	class Meta:
		template = 'blocks/recent_news_block.html'
		icon = 'fa-newspaper-o'
		label = 'Recent Press Releases'
