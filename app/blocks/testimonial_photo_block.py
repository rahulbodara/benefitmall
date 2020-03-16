from wagtail.core.blocks import CharBlock, StructBlock, TextBlock
from wagtail.images.blocks import ImageChooserBlock

from app.choices import SWITCHABLE_CHOICES
from app.widgets import CustomRadioSelect
from .custom_choice_block import CustomChoiceBlock
from .background_block import BackgroundBlock


class TestimonialPhotoBlock(StructBlock):
	image = ImageChooserBlock(required=True)
	quote = TextBlock()
	name = CharBlock()
	title = TextBlock()
	layout = CustomChoiceBlock(choices=SWITCHABLE_CHOICES, default=SWITCHABLE_CHOICES[0][0], required=False, widget=CustomRadioSelect)
	background = BackgroundBlock()

	class Meta:
		template = 'blocks/testimonial_photo_block.html'
		label = 'Testimonial Photo'
		icon = 'fa-user-circle-o'
