from wagtail.core.blocks import StreamBlock, StructBlock, TextBlock, ListBlock, CharBlock, IntegerBlock
from wagtail.images.blocks import ImageChooserBlock

from .link_block import LinkBlock
from app.choices import  SWITCHABLE_CHOICES, PRICING_FEATURE_CHOICES
from app.widgets import CustomRadioSelect
from .custom_choice_block import CustomChoiceBlock
from .background_block import BackgroundBlock

class FeatureBlock(StructBlock):
    spec = CharBlock(required=False)

    class Meta:
        form_classname = 'features-block'


class TestimonialBlock(StructBlock):
    image = ImageChooserBlock(required=False)
    testimonial_name = CharBlock(required=False, label='Name')
    testimonial = TextBlock(required=False)
    testimonial_location = CharBlock(required=False, label='Location')

    class Meta:
        form_classname = 'testimonial-block'


class PricingBlock(StructBlock):
    layout = CustomChoiceBlock(choices=PRICING_FEATURE_CHOICES, widget=CustomRadioSelect, default=PRICING_FEATURE_CHOICES[0][0])
    switchable = CustomChoiceBlock(choices=SWITCHABLE_CHOICES, default=SWITCHABLE_CHOICES[0][0], widget=CustomRadioSelect)
    title = CharBlock(required=False)
    price = IntegerBlock(required=False)
    fine_print = CharBlock(required=False)
    header = TextBlock(required=False)
    small_text = TextBlock(required=False)
    features = ListBlock(FeatureBlock)
    link_text = CharBlock(required=False)
    link_url = CharBlock(required=False)
    testimonial = TestimonialBlock(required=False)
    background = BackgroundBlock()

    class Meta:
        template = 'blocks/pricing_block.html'
        label = 'Pricing'
        icon = 'fa-usd'
        form_classname = 'pricing-block struct-block'

