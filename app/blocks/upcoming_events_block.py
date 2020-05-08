from wagtail.core.blocks import StructBlock
from wagtail.snippets.blocks import SnippetChooserBlock

from app.choices.block_edit_choices import MAX_ITEMS_CHOICES
from app.choices.model_choices import EVENT_LOCATION_TYPE_CHOICES
from app.widgets import CustomRadioSelect

from .background_block import BackgroundBlock
from .custom_choice_block import CustomChoiceBlock


class UpcomingEventsBlock(StructBlock):
	event_type = SnippetChooserBlock(label='Event Type', target_model='app.EventType', required=False, help_text='Optional. Leave blank to include all event types.')
	location_type = CustomChoiceBlock(label='Location Type', choices=EVENT_LOCATION_TYPE_CHOICES, default=EVENT_LOCATION_TYPE_CHOICES[0][0], required=False, widget=CustomRadioSelect)
	max_items = CustomChoiceBlock(label='Max Items', choices=MAX_ITEMS_CHOICES, default=MAX_ITEMS_CHOICES[0][0], required=False, widget=CustomRadioSelect)
	background = BackgroundBlock()

	class Meta:
		template = 'blocks/upcoming_events_block.html'
		icon = 'fa-calendar'
		label = 'Upcoming Events'
