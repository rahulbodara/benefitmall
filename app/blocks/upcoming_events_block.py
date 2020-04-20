from wagtail.core.blocks import StaticBlock


class UpcomingEventsBlock(StaticBlock):
	class Meta:
		admin_text = 'Automatically displays the 3 upcoming events.'
		template = 'blocks/upcoming_events_block.html'
		icon = 'fa-calendar'
		label = 'Upcoming Events'
