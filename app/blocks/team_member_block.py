from wagtail.core.blocks import StructBlock, CharBlock, TextBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock
from app.choices import SWITCHABLE_CHOICES, PARAGRAPH_SIZE_CHOICES
from app.widgets import CustomRadioSelect
from .custom_choice_block import CustomChoiceBlock


class TeamMemberBlock(StructBlock):
    layout = CustomChoiceBlock(choices=SWITCHABLE_CHOICES, default=SWITCHABLE_CHOICES[0][0], required=False, widget=CustomRadioSelect)
    name = CharBlock()
    title = CharBlock(required=False)
    image = ImageChooserBlock(required=False)
    body = RichTextBlock(required=False, features=['bold', 'italic', 'ol', 'ul', 'link', 'document-link'])
    body_size = CustomChoiceBlock(choices=PARAGRAPH_SIZE_CHOICES, default=PARAGRAPH_SIZE_CHOICES[1][0], required=False, widget=CustomRadioSelect, label='Body Size')

    social_mail = CharBlock(required=False, label='Email Address')
    social_facebook = CharBlock(required=False, label='Facebook Link')
    social_instagram = CharBlock(required=False, label='Instagram Link')
    social_twitter = CharBlock(required=False, label='Twitter Link')
    social_linkedin = CharBlock(required=False, label='Linkedin Link')
    social_youtube = CharBlock(required=False, label='Youtube Link')

    class Meta:
        template = 'blocks/team_member_block.html'
        label = 'Team Member'
        icon = 'fa-user'

