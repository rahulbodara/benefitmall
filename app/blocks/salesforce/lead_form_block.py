from wagtail.core.blocks import RichTextBlock, StructBlock, CharBlock, StreamBlockValidationError, ChoiceBlock
from app.widgets import CustomRadioSelect
from app.blocks.custom_choice_block import CustomChoiceBlock
from app.choices import HORIZONTAL_ALIGNMENT_CHOICES, SUBHEAD_SIZE_CHOICES

LEAD_OWNER_CHOICES = (
	('00Gc0000004I4ZuEAK', 'Paul McCartney'),
	('00Gc0000004I4ZuEAL', 'John Lennon'),
	('00Gc0000004I4ZuEAM', 'George Harrison'),
	('00Gc0000004I4ZuEAN', 'Ringo Starr'),
)
FORM_WIDTH_CHOICES = (
	('col-md-4', 'Small'),
	('col-md-6', 'Med'),
	('col-md-12', 'Large'),
)


class LeadFormBlock(StructBlock):
	alignment = CustomChoiceBlock(
		choices=HORIZONTAL_ALIGNMENT_CHOICES,
		default=HORIZONTAL_ALIGNMENT_CHOICES[0][0],
		required=False,
		widget=CustomRadioSelect)
	heading = CharBlock(
		max_length=512,
		required=False)
	heading_size = CustomChoiceBlock(
		choices=SUBHEAD_SIZE_CHOICES,
		default=SUBHEAD_SIZE_CHOICES[0][0],
		required=False,
		widget=CustomRadioSelect,
		label='Heading Size')
	body = RichTextBlock(
		required=False,
		features=['bold', 'italic', 'ol', 'ul', 'link', 'document-link'])
	form_width = CustomChoiceBlock(
		choices=FORM_WIDTH_CHOICES,
		default=FORM_WIDTH_CHOICES[0][0],
		required=False,
		widget=CustomRadioSelect,
		label='Form Width')
	lead_owner = ChoiceBlock(
		choices=LEAD_OWNER_CHOICES,
		default=LEAD_OWNER_CHOICES[0][0],
		required=True)

	class Meta:
		template = 'salesforce/lead_form_block.html'
		icon = 'fa-drivers-license-o'
		label = 'Lead Form'
		form_classname = 'lead-form-block struct-block'
