from wagtail.core.blocks import StreamBlock, StructBlock, CharBlock, ListBlock, BooleanBlock, IntegerBlock, URLBlock
from wagtail.images.blocks import ImageChooserBlock

from app.blocks.custom_choice_block import CustomChoiceBlock
from app.choices import GALLERY_MODE_CHOICES
from app.widgets import CustomRadioSelect
from .background_block import BackgroundBlock

class ProductBlock(StructBlock):
    product = CharBlock(required=True)
    purpose = CharBlock(required=True)
    price = IntegerBlock(required=True)
    buy_link = URLBlock(required=False)
    image = ImageChooserBlock(required=True)


class CategoryBlock(StructBlock):
    name = CharBlock(required=True)
    filter = CharBlock(required=True, help_text="All lowercase, substitute spaces with a '-'. ")
    products = ListBlock(ProductBlock)


class ProductsBlock(StructBlock):
    categories = ListBlock(CategoryBlock)
    background = BackgroundBlock()
    class Meta:
        icon = 'fa-credit-card'
        template = 'blocks/products_block.html'
        label = 'Products Block'
