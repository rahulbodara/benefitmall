from wagtail.core.blocks import StructBlock, StructValue
from wagtail.images.blocks import ImageChooserBlock

from app.choices import SWITCHABLE_CHOICES, VERTICAL_ALIGNMENT_CHOICES, MEDIA_TITLE_LAYOUT_CHOICES
from app.widgets import CustomRadioSelect
from .custom_choice_block import CustomChoiceBlock
from .background_block import BackgroundBlock
from .media_block import MediaBlock
from .multi_text_block import MultiTextBlock


class MediaTitleBlock(StructBlock):
    layout = CustomChoiceBlock(choices=MEDIA_TITLE_LAYOUT_CHOICES, default=MEDIA_TITLE_LAYOUT_CHOICES[0][0], required=False, widget=CustomRadioSelect)
    switchable = CustomChoiceBlock(choices=SWITCHABLE_CHOICES, default=SWITCHABLE_CHOICES[0][0], required=False, widget=CustomRadioSelect)
    media = MediaBlock()
    small_image = ImageChooserBlock(required=False, label='Small Image')
    vertical_alignment = CustomChoiceBlock(choices=VERTICAL_ALIGNMENT_CHOICES, default=VERTICAL_ALIGNMENT_CHOICES[0][0], required=False, widget=CustomRadioSelect, label='Vertical Alignment')
    text = MultiTextBlock()
    background = BackgroundBlock()

    class Meta:
        icon = 'fa-id-card'
        template = 'blocks/media_title_block.html'
        label = 'Media + Title'
        form_classname = 'media-title-block struct-block'
