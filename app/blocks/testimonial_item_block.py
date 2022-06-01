from wagtail.core.blocks import CharBlock, StructBlock, TextBlock
from wagtail.images.blocks import ImageChooserBlock


class TestimonialItemBlock(StructBlock):
    name = CharBlock()
    location = CharBlock()
    testimonial = TextBlock()
    image = ImageChooserBlock(required=False)

    class Meta:
        template = 'blocks/testimonial_item_block.html'
        label = 'Testimonial'
        icon = 'doc-full-inverse'
