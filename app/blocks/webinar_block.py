from wagtail.core.blocks import StructBlock, StaticBlock
from app.blocks.background_block import BackgroundBlock


class WebinarBlock(StructBlock):
    text = StaticBlock(admin_text='This block will show 3 most recent webinars, with a link to all webinars')
    background = BackgroundBlock()

    class Meta:
        template = 'blocks/webinar_block.html'
        icon = 'fa-video-camera'
        form_classname = 'webinar-block struct-block'
