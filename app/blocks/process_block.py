from wagtail.core.blocks import StreamBlock, StructBlock

from app.choices import PROCESS_BLOCK_LAYOUT_CHOICES, SWITCHABLE_CHOICES
from app.widgets import CustomRadioSelect
from .custom_choice_block import CustomChoiceBlock
from .process_item_block import ProcessItemBlock
from .background_block import BackgroundBlock
# from .media_block import MediaBlock
from .vidyard_media_block import MediaBlock


class ProcessBlock(StructBlock):
    process_layout = CustomChoiceBlock(label='Layout', choices=PROCESS_BLOCK_LAYOUT_CHOICES, default=PROCESS_BLOCK_LAYOUT_CHOICES[0][0], required=True, widget=CustomRadioSelect)
    process_media = MediaBlock(label='Image or Video', )
    process_orientation = CustomChoiceBlock(label='Orientation', choices=SWITCHABLE_CHOICES, default=SWITCHABLE_CHOICES[0][0], required=False, widget=CustomRadioSelect)
    process_items = StreamBlock([('processitem', ProcessItemBlock())], label='Items', required=True)
    process_background = BackgroundBlock(label='Background', )

    class Meta:
        template = 'blocks/process_block.html'
        label = 'Process / Timeline'
        icon = 'fa-sitemap'
        form_classname = 'process-block struct-block'

