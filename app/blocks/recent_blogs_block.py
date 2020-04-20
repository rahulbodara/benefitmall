from wagtail.core.blocks import StaticBlock


class RecentBlogsBlock(StaticBlock):
	class Meta:
		admin_text = 'Automatically displays the 3 most recent blog posts.'
		template = 'blocks/recent_blogs_block.html'
		icon = 'fa-rss'
		label = 'Recent Blogs'
