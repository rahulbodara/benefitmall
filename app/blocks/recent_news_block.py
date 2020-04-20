from wagtail.core.blocks import StaticBlock


class RecentNewsBlock(StaticBlock):
	class Meta:
		admin_text = 'Automatically displays the 3 most recent press releases.'
		template = 'blocks/recent_news_block.html'
		icon = 'fa-newspaper-o'
		label = 'Recent Press Releases'
