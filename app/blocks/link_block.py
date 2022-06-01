from django.forms.utils import ErrorList

from wagtail.core.models import Page
from wagtail.core.blocks import CharBlock, EmailBlock, PageChooserBlock, StructValue, StructBlock, StreamBlock, StreamBlockValidationError
from wagtail.documents.blocks import DocumentChooserBlock

from app.widgets import CustomRadioSelect
from app.blocks.custom_choice_block import CustomChoiceBlock
from app.choices import LINK_TYPE_CHOICES, LINK_FORMAT_CHOICES


class LinkBlockStructValue(StructValue):
    def href(self):
        """
        Return extra values to the template context.
        """
        link_type = self.get('link_type')
        href = self.get(link_type)
        if link_type == 'page':
            return href.url
        if link_type == 'document':
            return href.file.url
        return href

    def href_prefix(self):
        """
        Return extra values to the template context.
        """
        link_type = self.get('link_type')
        prefix = ''
        if link_type == 'phone':
            prefix = 'tel:'
        if link_type == 'email':
            prefix = 'mailto:'
        return prefix

    def title_attribute(self):
        """
        Return extra values to the template context.
        """
        # TODO - Add additional attributes here for other link types.

        link_type = self.get('link_type')
        title = ''
        if link_type == 'document':
            doc = self.get('document')
            title = doc.title
        return title

    def target(self):
        link_type = self.get('link_type')
        if link_type == 'document' or link_type == 'url':
            return '_blank'
        else:
            return '_self'

class LinkBlock(StructBlock):
    link_type = CustomChoiceBlock(label='Type', choices=LINK_TYPE_CHOICES, default=LINK_TYPE_CHOICES[0][0], required=False, widget=CustomRadioSelect)
    url = CharBlock(label='URL', required=False)
    page = PageChooserBlock(required=False)
    document = DocumentChooserBlock(required=False)
    email = EmailBlock(required=False)
    phone = CharBlock(required=False)
    link_text = CharBlock(label='Text', required=False)
    link_format = CustomChoiceBlock(label='Format', choices=LINK_FORMAT_CHOICES, default=LINK_FORMAT_CHOICES[0][0], required=False, widget=CustomRadioSelect)

    def clean(self, value):
        """
        Override to conditionally require the appropriate link field. See global.js for client-side validation.
        """
        value = super(LinkBlock, self).clean(value)
        values = {f: v for f, v in value.items()}
        link_type = values['link_type']
        errors = {}
        if link_type:
            for field in [link_type, 'link_text']:
                if not values[field]:
                    errors[field] = ErrorList(['This field is required.'])
        if errors:
            raise StreamBlockValidationError(block_errors=errors)
        return value

    class Meta:
        template = 'blocks/link_block.html'
        icon = 'fa-link'
        value_class = LinkBlockStructValue
        form_classname = 'link-block struct-block'
