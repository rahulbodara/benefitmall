from wagtail.core.blocks import StreamBlock, StructBlock, CharBlock, ListBlock, BooleanBlock
from wagtail.images.blocks import ImageChooserBlock

from app.blocks.custom_choice_block import CustomChoiceBlock
from app.choices import GALLERY_MODE_CHOICES
from app.widgets import CustomRadioSelect
from .background_block import BackgroundBlock


class ImageBlock(StructBlock):
    title = CharBlock(required=False)
    subtitle = CharBlock(required=False)
    image = ImageChooserBlock(required=True)


class CategoryBlock(StructBlock):
    name = CharBlock(required=True)
    filter = CharBlock(required=True, help_text="All lowercase, substitute spaces with a '-'. ")
    images = ListBlock(ImageBlock)


class GalleryBlock(StructBlock):
    mode = CustomChoiceBlock(choices=GALLERY_MODE_CHOICES, widget=CustomRadioSelect)
    hover = BooleanBlock(required=False, label='Mouse Hover', help_text='If selected overlay text will appear when hovered by mouse.')
    categories = ListBlock(CategoryBlock)
    background = BackgroundBlock()

    class Meta:
        icon = 'fa-camera'
        form_classname = 'gallery-block struct-block'
        template = 'blocks/gallery_block.html'
        label = 'Gallery Block'
