from django.conf import settings
from django.conf.urls import url
from django.templatetags.static import static
from django.urls import reverse
from django.utils.html import format_html
from django.db import models

from wagtail.core import hooks
from wagtail.admin.menu import MenuItem
from wagtail.contrib.modeladmin.options import ModelAdmin, ModelAdminGroup, modeladmin_register
from wagtail.contrib.settings.models import BaseSetting, register_setting

from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, FieldPanel, MultiFieldPanel, StreamFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.core.fields import StreamField

from app.views import IconReference
from app.models import Icon

from wagtail.core.fields import RichTextField
from app.choices import NAVIGATION_CHOICES, FOOTER_CHOICES
from app.blocks.stream_blocks import HeaderLinkStreamBlock, HeaderButtonStreamBlock, FooterLinkStreamBlock, FooterButtonStreamBlock, FooterUtilityLinkStreamBlock, FooterCategoryLinkStreamBlock

from app.models.events import Event, EventRegistration

@register_setting(icon='cogs')
class HeaderFooter(BaseSetting):
    class Meta:
        verbose_name = 'Header & Footer'

    # General
    header_logo = models.ForeignKey(
        'wagtailimages.Image', models.SET_NULL, blank=True, null=True,
        help_text='Logo used in header. Recommended transparent PNG',
        related_name='header_logo')
    footer_logo = models.ForeignKey(
        'wagtailimages.Image', models.SET_NULL, blank=True, null=True,
        help_text='Logo used in header. Recommended transparent PNG',
        related_name='footer_logo')
    social_facebook = models.CharField(
        null=True, blank=True, default='',
        max_length=250,
        verbose_name='Facebook Link',
        help_text='Enter your Facebook link here.')
    social_instagram = models.CharField(
        null=True, blank=True, default='',
        max_length=250,
        verbose_name='Instagram Link',
        help_text='Enter your Instagram link here.')
    social_twitter = models.CharField(
        null=True, blank=True, default='',
        max_length=250,
        verbose_name='Twitter Link',
        help_text='Enter your Twitter link here.')
    social_linkedin = models.CharField(
        null=True, blank=True, default='',
        max_length=250,
        verbose_name='LinkedIn Link',
        help_text='Enter your LinkedIn link here.')
    social_youtube = models.CharField(
        null=True, blank=True, default='',
        max_length=250,
        verbose_name='YouTube Link',
        help_text='Enter your YouTube link here.')

    copyright_text = models.CharField(
        null=True, blank=True, default='',
        max_length=250,
        verbose_name='Copyright text',
        help_text='Enter the text that should appear after the year in the copyright line.')
    tagline = models.CharField(
        null=True, blank=True, default='',
        max_length=250,
        verbose_name='Tagline text',
        help_text='Enter the text that should appear in the tag line.')

    general_tab_panels = [
        MultiFieldPanel([
            ImageChooserPanel('header_logo'),
            ImageChooserPanel('footer_logo'),

        ], heading='Logos', classname='collapsible'),
        MultiFieldPanel([
            FieldPanel('social_facebook'),
            FieldPanel('social_instagram'),
            FieldPanel('social_twitter'),
            FieldPanel('social_linkedin'),
            FieldPanel('social_youtube'),
        ], heading='Social Media', classname='collapsible'),
        MultiFieldPanel([
            FieldPanel('copyright_text'),
            FieldPanel('tagline'),
        ], heading='Copyright', classname='collapsible'),
    ]

    # Nav
    navigation_type = models.CharField(
        default=NAVIGATION_CHOICES[0][0],
        choices=NAVIGATION_CHOICES,
        max_length=50,
        verbose_name='Navigation Type',
        help_text='Choose a navigation style')
    header_automatic_nav = models.BooleanField(verbose_name='Automatic Nav', default=True, help_text='Automatically populate the nav with top-level menu pages')
    header_links = StreamField(HeaderLinkStreamBlock(required=False), verbose_name='Links', blank=True, null=True, help_text='Populate the nav with custom links')
    header_buttons = StreamField(HeaderButtonStreamBlock(required=False), verbose_name='Buttons', blank=True, null=True, help_text='Populate the nav with custom buttons')
    header_banner_text_1 = models.CharField(
        null=True, blank=True, default='',
        max_length=250,
        verbose_name='Banner Text Line 1',
        help_text='Enter one line of text')
    header_banner_text_2 = models.CharField(
        null=True, blank=True, default='',
        max_length=250,
        verbose_name='Banner Text Line 2',
        help_text='Enter one line of text')

    header_tab_panels = [
        MultiFieldPanel([
            FieldPanel('navigation_type'),
            FieldPanel('header_automatic_nav'),
            StreamFieldPanel('header_links'),
            StreamFieldPanel('header_buttons'),
            FieldPanel('header_banner_text_1'),
            FieldPanel('header_banner_text_2')
        ], heading='Navigation', classname='collapsible'),
    ]

    # Footer
    footer_type = models.CharField(
        default=FOOTER_CHOICES[0][0],
        choices=FOOTER_CHOICES,
        max_length=50,
        verbose_name='Footer Type',
        help_text='Choose a footer style')

    footer_links = StreamField(FooterLinkStreamBlock(required=False), verbose_name='Links', blank=True, null=True, help_text='Populate the footer with custom links')
    footer_buttons = StreamField(FooterButtonStreamBlock(required=False), verbose_name='Buttons', blank=True, null=True, help_text='Populate the footer with custom buttons')
    footer_utility_links = StreamField(FooterUtilityLinkStreamBlock(required=False), verbose_name='Utility Links', blank=True, null=True, help_text='Populate the utility footer with custom links')
    footer_category_links = StreamField(FooterCategoryLinkStreamBlock(required=False), verbose_name='Categorized Links', blank=True, null=True, help_text='Populate the footer with categorized links')

    footer_tab_panels = [
        MultiFieldPanel([
            FieldPanel('footer_type'),
            StreamFieldPanel('footer_links'),
            StreamFieldPanel('footer_buttons'),
            StreamFieldPanel('footer_utility_links'),
            StreamFieldPanel('footer_category_links'),
        ], heading='Footer', classname='collapsible'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(general_tab_panels, heading='General'),
        ObjectList(header_tab_panels, heading='Header'),
        ObjectList(footer_tab_panels, heading='Footer'),
    ])



class IconAdmin(ModelAdmin):
    model = Icon
    list_display = ['get_title', 'get_glyph', 'category']
    list_filter = ['category']
    list_per_page = 100
    search_fields = ['title']
    empty_value_display = ''
    menu_icon = 'icon icon-list-ul'
    menu_order = 10000
    add_to_settings_menu = True

    def get_title(self, obj):
        view_url = reverse('wagtailadmin_explore', args=[obj.id])
        return format_html('<h2><a href="{}">{}</a></h2>'.format(view_url, obj))
    get_title.short_description = 'Title'
    get_title.admin_order_field = 'title'

    def get_extra_class_names_for_field_col(self, obj, field_name):
        if field_name == 'get_title':
            return ['title']
        return []

    def get_glyph(self, obj):
        return format_html('<i class="glyph">&#x{}</i>'.format(obj.unicode_value))
    get_glyph.short_description = 'Glyph'

    def get_extra_class_names_for_field_col(self, obj, field_name):
        if field_name == 'get_title':
            return ['title']
        return []

modeladmin_register(IconAdmin)


# Insert global admin CSS
@hooks.register('insert_global_admin_css')
def global_admin_css():
    return format_html('<link rel="stylesheet" href="{}">', static('css/admin/global.css'))


# Insert global admin JS
@hooks.register('insert_global_admin_js')
def global_admin_js():
    # Returns HTML/Javascript to the admin template
    scripts = ''

    # Returns language selector UI if there are multiple languages
    if len(settings.LANGUAGES) > 1:
        scripts += """
            <script>
                var langs_obj = {languages};
            </script>
            """.format(languages=dict(settings.LANGUAGES))

        scripts += format_html('<script src="{}"></script>', static('js/admin/language_selector.js'))

    # Returns general scripts
    scripts += format_html('<script src="{}"></script>', static('js/admin/global.js'))
    scripts += format_html('<script src="{}"></script>', static('js/admin/header_footer.js'))
    return scripts


# Add Icon Reference to admin urls
@hooks.register('register_admin_urls')
def url_icon_reference():
    return [url(r'^icon-reference/$', IconReference.as_view(), name='icon-reference'),]


# Add Icon Reference in Settings menu
@hooks.register('register_settings_menu_item')
def register_icon_reference_menu_item():
    return MenuItem('Icon Reference', reverse('icon-reference'), classnames='icon icon-view', order=9998)


# @register_setting(icon = 'download')
# class ErrorPages(BaseSetting):
#     title_404 = models.TextField(default='404 not found', null=True, blank=True)
#     body_404 = RichTextField(null=True, blank=True)


class EventAdmin(ModelAdmin):
    model = Event
    menu_label = 'Events'
    menu_icon = 'date'
    list_display = ('event_title', 'event_type', 'location_type', 'start_datetime', )
    list_filter = ('location_type', 'event_type', 'address_city', 'address_state', )
    search_fields = ('event_title', 'address_city', 'address_state', 'description', )


class EventRegistrationAdmin(ModelAdmin):
    model = EventRegistration
    menu_label = 'Event Registrations'
    menu_icon = 'group'

    list_display = ('get_title', 'get_date', 'first_name', 'last_name', 'postalcode')

    def get_title(self, obj: EventRegistration):
        return obj.event.event_title
    get_title.short_description = 'Event Name'
    get_title.admin_order_field = 'Event Name'

    def get_date(self, obj: EventRegistration):
        return obj.event.start_datetime.strftime('%m/%d/%Y')
    get_date.short_description = 'Event date'
    get_date.admin_order_field = 'EVent Date'


class EventsAdminGroup(ModelAdminGroup):
    menu_label = 'Events'
    menu_icon = 'date'
    items = (EventAdmin, EventRegistrationAdmin)

modeladmin_register(EventsAdminGroup)

