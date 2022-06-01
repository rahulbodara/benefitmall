from wagtail.core.blocks import StreamBlock, StructBlock, BooleanBlock
from .background_block import BackgroundBlock
from app.choices.block_edit_choices import BIO_LAYOUT_CHOICES, SUBHEAD_SIZE_CHOICES
from app.widgets import CustomRadioSelect
from .custom_choice_block import CustomChoiceBlock

PERSON_BLOCK_CHOICES = (
    ('all', 'All People'),
    ('executives', 'Executives Only'),
	('sales', 'Sales Leadership Only'),
)

class PersonListBlock(StructBlock):
	layout = CustomChoiceBlock(choices=BIO_LAYOUT_CHOICES, default=BIO_LAYOUT_CHOICES[0][0], required=True, widget=CustomRadioSelect)
	executives = CustomChoiceBlock(choices=PERSON_BLOCK_CHOICES, default=PERSON_BLOCK_CHOICES[0][0], required=True, widget=CustomRadioSelect)
	title_size = CustomChoiceBlock(choices=SUBHEAD_SIZE_CHOICES, default=SUBHEAD_SIZE_CHOICES[0][0], required=False, widget=CustomRadioSelect, label='Title Size')
	background = BackgroundBlock()

	class Meta:
		icon = 'fa-users'
		template = 'blocks/person_list_block.html'
		label = 'Person List'
