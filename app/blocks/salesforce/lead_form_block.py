from wagtail.core.blocks import StructValue, StructBlock, CharBlock, StreamBlockValidationError, ChoiceBlock

LEAD_OWNER_CHOICES = (
	('00Gc0000004I4ZuEAK', 'Paul McCartney'),
	('00Gc0000004I4ZuEAL', 'John Lennon'),
	('00Gc0000004I4ZuEAM', 'George Harrison'),
	('00Gc0000004I4ZuEAN', 'Ringo Starr'),
)


class LeadFormBlock(StructBlock):
	lead_owner = ChoiceBlock(choices=LEAD_OWNER_CHOICES, default=LEAD_OWNER_CHOICES[0][0], required=True)

	class Meta:
		template = 'salesforce/lead_form_block.html'
		icon = 'fa-drivers-license-o'
		label = 'Lead Form'
		form_classname = 'lead-form-block struct-block'
