from django.forms.utils import ErrorList

from wagtail.core.models import Page
from wagtail.core.blocks import CharBlock, EmailBlock, PageChooserBlock, StructValue, StructBlock, StreamBlock, StreamBlockValidationError
from wagtail.documents.blocks import DocumentChooserBlock

from app.widgets import CustomRadioSelect
from app.blocks.custom_choice_block import CustomChoiceBlock
from app.choices import LINK_TYPE_CHOICES, LINK_FORMAT_CHOICES
from app.blocks.link_block import LinkBlock

class CategoryLinkBlock(StructBlock):
    category_label = CharBlock(label='Category Name', required=False)
    links = StreamBlock([('link', LinkBlock())], label='link', required=True)



    class Meta:
        template = 'blocks/link_block.html'
        icon = 'fa-link'
        form_classname = 'link-block struct-block'