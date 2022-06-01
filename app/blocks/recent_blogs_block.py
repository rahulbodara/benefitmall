from wagtail.core.blocks import StructBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from app.choices.block_edit_choices import MAX_ITEMS_CHOICES
from app.widgets import CustomRadioSelect

from .background_block import BackgroundBlock
from .custom_choice_block import CustomChoiceBlock


class RecentBlogsBlock(StructBlock):
	category = SnippetChooserBlock(label='Blog Category', target_model='app.BlogCategory', required=False, help_text='Optional. Leave blank to include all categories.')
	max_items = CustomChoiceBlock(label='Max Items', choices=MAX_ITEMS_CHOICES, default=MAX_ITEMS_CHOICES[0][0], required=False, widget=CustomRadioSelect)
	background = BackgroundBlock()

	class Meta:
		template = 'blocks/recent_blogs_block.html'
		icon = 'fa-rss'
		label = 'Recent Blogs'
