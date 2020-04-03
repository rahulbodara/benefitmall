from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.models import AbstractFormField
from wagtail.core.blocks import StructValue, StructBlock, CharBlock, ListBlock, RichTextBlock
from app.blocks.custom_choice_block import CustomChoiceBlock
from django.utils.http import urlencode
from django.db import models


class EmbeddedMapStructValue(StructValue):
    def framesource(self):
        address = '{} {} {}, {}'.format(self.get('address'), self.get('city'), self.get('state'), self.get('zip_code'))
        address = 'https://maps.google.com/maps?'+urlencode({'q': address, 'output': 'embed'})
        return address


class ContactMapBlock(StructBlock):
    title = CharBlock(required=True)
    address = CharBlock(required=True)
    city = CharBlock(required=True)
    state = CharBlock(required=True)
    zip_code = CharBlock(required=True)
    direct_phone = CharBlock(required=False)
    toll_free_phone = CharBlock(required=False)
    wysiwyg = RichTextBlock(required=False)
    class Meta:
        icon = 'search'
        template = 'blocks/contact_map_block.html'
        value_class = EmbeddedMapStructValue
