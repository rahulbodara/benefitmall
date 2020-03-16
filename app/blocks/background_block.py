from django.forms.utils import ErrorList

from wagtail.core.blocks import StructValue, StructBlock, StreamBlockValidationError
from wagtail.images.blocks import ImageChooserBlock

from app.widgets import CustomRadioSelect
from app.choices import BACKGROUND_MODE_CHOICES, IMAGE_EFFECT_CHOICES, IMAGE_INVERT_CHOICES, IMAGE_OVERLAY_CHOICES, PADDING_CHOICES, BACKGROUND_SIZE_CHOICES, BACKGROUND_SIZING_MODE
from .custom_choice_block import CustomChoiceBlock


class BackgroundBlockStructValue(StructValue):
    def classes(self):
        """
        Return extra values to the template context.
        """
        classes = []
        if self.get('sizing_mode') == 'percent':
            if self.get('sizing'):
                classes.append('cover')
                classes.append(self.get('sizing'))
        else:
            if self.get('padding'):
                classes.append(self.get('padding'))
        if self.get('mode'):
            classes.append(self.get('mode'))
        if self.get('mode') == 'imagebg':
            if self.get('image_effect'):
                classes.append(self.get('image_effect'))
            if self.get('image_invert'):
                classes.append(self.get('image_invert'))
        return ' '.join(classes)

    def data_image_overlay(self):
        """
        Return extra values to the template context.
        """
        if self.get('mode') == 'imagebg':
            return 'data-overlay={}'.format(self.get('image_overlay'))
        else:
            return ''

    def size_mode(self):
        """
        Return extra values to the template context.
        """
        if self.get('sizing_mode') == 'percent':
            return 'pos-vertical-center'
        else:
            return ''


class BackgroundBlock(StructBlock):
    mode = CustomChoiceBlock(choices=BACKGROUND_MODE_CHOICES, default=BACKGROUND_MODE_CHOICES[0][0], required=False, widget=CustomRadioSelect)
    background_image = ImageChooserBlock(required=False)
    image_effect = CustomChoiceBlock(choices=IMAGE_EFFECT_CHOICES, default=IMAGE_EFFECT_CHOICES[0][0], required=False, widget=CustomRadioSelect, label='Image Effect')
    image_invert = CustomChoiceBlock(choices=IMAGE_INVERT_CHOICES, default=IMAGE_INVERT_CHOICES[0][0], required=False, widget=CustomRadioSelect, label='Invert Dark/Light')
    image_overlay = CustomChoiceBlock(choices=IMAGE_OVERLAY_CHOICES, default='4', required=False, widget=CustomRadioSelect, label='Overlay Opacity')
    sizing_mode = CustomChoiceBlock(choices=BACKGROUND_SIZING_MODE, default=BACKGROUND_SIZING_MODE[0][0], required=False, widget=CustomRadioSelect)
    padding = CustomChoiceBlock(choices=PADDING_CHOICES, default=PADDING_CHOICES[3][0], required=False, widget=CustomRadioSelect)
    sizing = CustomChoiceBlock(choices=BACKGROUND_SIZE_CHOICES, default=BACKGROUND_SIZE_CHOICES[4][0], required=False, widget=CustomRadioSelect)

    def clean(self, value):
        """
        Override to conditionally require the image field. See global.js for client-side validation.
        """
        value = super(BackgroundBlock, self).clean(value)
        values = {f: v for f, v in value.items()}
        mode = values['mode']
        errors = {}
        if mode == 'imagebg' and not values['background_image']:
            errors['background_image'] = ErrorList(['This field is required.'])
        if errors:
            raise StreamBlockValidationError(block_errors=errors)
        return value

    class Meta:
        template = 'blocks/background_block.html'
        form_classname = 'background-block struct-block'
        value_class = BackgroundBlockStructValue
