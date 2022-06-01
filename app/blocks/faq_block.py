from wagtail.core.blocks import StreamBlock, StructBlock, CharBlock

from .faq_item_block import FAQItemBlock
from .background_block import BackgroundBlock


class FAQBlock(StructBlock):
    title = CharBlock()
    faqs_col1 = StreamBlock([('faqitem', FAQItemBlock())], label='FAQs Column 1', required=True)
    faqs_col2 = StreamBlock([('faqitem', FAQItemBlock())], label='FAQs Column 2', required=True)
    background = BackgroundBlock()

    class Meta:
        icon = 'fa-question-circle-o'
        template = 'blocks/faq_block.html'
        label = 'FAQ List'
