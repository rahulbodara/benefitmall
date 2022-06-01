from wagtail.core.blocks import StructBlock, StaticBlock
from app.blocks.background_block import BackgroundBlock


class PodcastBlock(StructBlock):
    text = StaticBlock(admin_text='This block will show 3 most recent podcast, with a link to all podcast')
    background = BackgroundBlock()

    class Meta:
        template = 'blocks/podcast_block.html'
        icon = 'fa-podcast'
        form_classname = 'podcast-block struct-block'
