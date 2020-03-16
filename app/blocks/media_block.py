from django.forms.utils import ErrorList

from wagtail.core.blocks import StructValue, StructBlock, CharBlock, StreamBlockValidationError
from wagtail.images.blocks import ImageChooserBlock

from app.widgets import CustomRadioSelect
from app.choices import MEDIA_MODE_CHOICES, VIDEO_SOURCE_CHOICES, MEDIA_CORNERS_CHOICES, MEDIA_SHADOW_CHOICES
from .custom_choice_block import CustomChoiceBlock


class MediaBlock(StructBlock):
    mode = CustomChoiceBlock(choices=MEDIA_MODE_CHOICES, default=MEDIA_MODE_CHOICES[0][0], required=False, widget=CustomRadioSelect)
    image = ImageChooserBlock()
    video_source = CustomChoiceBlock(choices=VIDEO_SOURCE_CHOICES, default=VIDEO_SOURCE_CHOICES[0][0], required=False, widget=CustomRadioSelect, label='Video Source')
    video_id = CharBlock(required=False, label='Video ID', help_text='Enter the video source ID from YouTube or Vimeo. Should only consist of alphanumeric characters. Ex: 86036070')
    corners = CustomChoiceBlock(choices=MEDIA_CORNERS_CHOICES, default=MEDIA_CORNERS_CHOICES[0][0], required=False, widget=CustomRadioSelect, label='Corners')
    shadow = CustomChoiceBlock(choices=MEDIA_SHADOW_CHOICES, default=MEDIA_SHADOW_CHOICES[0][0], required=False, widget=CustomRadioSelect, label='Shadow')

    def clean(self, value):
        """
        Override to conditionally require the image field. See global.js for client-side validation.
        """
        value = super(MediaBlock, self).clean(value)
        values = {f: v for f, v in value.items()}
        mode = values['mode']
        errors = {}
        if mode == 'image-video' and not values['video_id']:
            errors['video_id'] = ErrorList(['This field is required.'])
        if errors:
            raise StreamBlockValidationError(block_errors=errors)
        return value

    class Meta:
        template = 'blocks/media_block.html'
        icon = 'fa-image'
        form_classname = 'media-block struct-block'
