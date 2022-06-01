from wagtail.core.blocks import StructBlock, CharBlock, TextBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock


class FAQItemBlock(StructBlock):
    question = CharBlock()
    answer = RichTextBlock()

    class Meta:
        template = 'blocks/faq_item_block.html'
        label = 'FAQ'
        icon = 'fa-question-circle-o'
