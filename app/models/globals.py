from django import forms
from django.db import models

from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface, FieldRowPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.models import Page
from wagtail.core.fields import StreamField

#from app.blocks import HeaderStreamBlock, FooterStreamBlock


# @register_setting(icon='cog')
# class GeneralSetting(BaseSetting):
#     # GENERAL
#     logo = models.ForeignKey('wagtailimages.Image', blank=True, null=True, help_text='Logo used in header, footer, and admin. Recommended transparent PNG', related_name='+')
#     favicon = models.ForeignKey('wagtailimages.Image', blank=True, null=True, help_text='Sizes: 16x16 / 32x32. Formats: PNG / GIF / ICO')
#     # - color scheme
#     # - typography
#     # - site chooser
#     # - from email
#     # HEADER
#     header = StreamField(HeaderStreamBlock(required=False), blank=True, null=True)
#     # FOOTER
#     footer = StreamField(FooterStreamBlock(required=False), blank=True, null=True)
#     # - Primary Link List
#     # - copyright_text 'Copyright text to follow automatic copyright symbol and current year.'
#     # - contact link 
#     # - Social
#     # Social
#     # - facebook_url 'Facebook page URL'
#     # - twitter_url 'Twitter account URL, without the @'
#     # - instagram_url 'Instagram account URL, without the @'
#     # - youtube_url 'YouTube channel or user account URL'
#     # - linkedin_url 'LinkedIn page URL'
#     # - google_url 'Google+ page or Google business listing URL'
#     # - background style
#     # SEO
#     gtm_tracking_id = models.CharField(verbose_name='GTM Tracking ID', max_length=100, null=True, blank=True, help_text='Google Tag Manager tracking identifcation number')
#     robots_txt = models.CharField(verbose_name='Robots.txt', max_length=1000, null=True, blank=True, help_text='')

#     general_panels = [
#         MultiFieldPanel([
#             ImageChooserPanel('logo'),
#             ImageChooserPanel('favicon'),
#             # FieldPanel('site_chooser'),
#             # FieldPanel('from_email'),
#         ], heading='General')
#     ]
#     header_panels = [
#         StreamFieldPanel('header'),
#     ]
#     footer_panels = [
#         StreamFieldPanel('footer'),
#     ]
#     seo_panels = [
#         MultiFieldPanel([
#             FieldPanel('gtm_tracking_id'),
#             FieldPanel('robots_txt', widget=forms.Textarea),
#         ], heading='SEO')
#     ]

#     edit_handler = TabbedInterface([
#         ObjectList(general_panels, heading='General'),
#         ObjectList(header_panels, heading='Header'),
#         ObjectList(footer_panels, heading='Footer'),
#         ObjectList(seo_panels, heading='SEO'),
#     ])

#     class Meta:
#         verbose_name = 'General'


class Icon(models.Model):
    CATEGORY_CHOICES = (
        ('1', 'Database'),
        ('2', 'Zodiacs'),
        ('3', 'Windows'),
        ('4', 'Weather'),
        ('5', 'Video'),
        ('6', 'User Interface'),
        ('7', 'Transportation'),
        ('8', 'Touch Gestures'),
        ('9', 'Time'),
        ('10', 'Text'),
        ('11', 'Sports'),
        ('12', 'Speech Bubbles'),
        ('13', 'Social Media'),
        ('14', 'Signs/Symbols'),
        ('15', 'Shopping/E-commerce'),
        ('16', 'SEO Icons'),
        ('17', 'Security'),
        ('18', 'Science/Medical'),
        ('19', 'Photos'),
        ('20', 'People'),
        ('21', 'Nature'),
        ('22', 'Objects'),
        ('23', 'Music'),
        ('24', 'Media Control'),
        ('25', 'Maps/Locations'),
        ('26', 'Logos'),
        ('27', 'Interface'),
        ('28', 'Industry'),
        ('29', 'Hipster Style'),
        ('30', 'Hardware'),
        ('31', 'Halloween'),
        ('32', 'Food/Drinks'),
        ('33', 'Folders'),
        ('34', 'Flags'),
        ('35', 'Files'),
        ('36', 'Emoticons'),
        ('37', 'Emails'),
        ('38', 'Education'),
        ('39', 'Desktop Apps'),
        ('40', 'Design'),
        ('41', 'Communications/Network'),
        ('42', 'Clothes/Accessories'),
        ('43', 'Cloud'),
        ('44', 'Chess'),
        ('45', 'Christmas'),
        ('46', 'Buildings/Landmarks'),
        ('47', 'Business/Finance'),
        ('48', 'Body Parts'),
        ('49', 'Browsers/Operating Systems'),
        ('50', 'Arrow View'),
        ('51', 'Arrows'),
        ('52', 'Alignment'),
        ('53', 'Animals'),
        ('54', 'Doctor'),
        ('55', 'Places'),
    )
    title = models.CharField(max_length=255, help_text='Warning: This title is also the exact classname used to reference the icon in the CSS.')
    unicode_value = models.CharField(max_length=255, default='', help_text='Warning: This unicode value is how the icon is referenced in the font file.')
    category = models.CharField(max_length=3, choices=CATEGORY_CHOICES, default='')

    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            FieldPanel('unicode_value'),
            FieldPanel('category'),
        ],
        heading="Icon",
        )
    ]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']
