from wagtail.core.blocks import StructBlock, CharBlock, TextBlock, PageChooserBlock
from wagtail.images.blocks import ImageChooserBlock


class BioListItemBlock(StructBlock):
    name = CharBlock()
    title = CharBlock(required=False)
    link = PageChooserBlock(required=False)
    image = ImageChooserBlock(required=False)

    class Meta:
        template = 'blocks/bio_list_item_block.html'
        label = 'Bio'
        icon = 'fa-user'
