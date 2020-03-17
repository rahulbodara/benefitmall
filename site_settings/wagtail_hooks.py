from django.db import models
from wagtail.admin.edit_handlers import TabbedInterface, ObjectList, FieldPanel, MultiFieldPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.images.models import Image


@register_setting(icon='password')
class SiteSettings(BaseSetting):
    # Analytics Tab
    google_analytics_tag = models.CharField(
        null=True, blank=True, default='',
        max_length=50,
        verbose_name='Tag Manager ID',
        help_text='Enter your GTM code here.')

    # Configuration Tab
    robots_txt = models.TextField(
        null=True, blank=True, default='User-agent: *\nDisallow: /',
        verbose_name='Robots.txt',
        help_text='Enter your robots.tx crawler instructions here')
    favicon_ico = models.ForeignKey(
        Image, models.SET_NULL, blank=True, null=True,
        help_text='The favicon must be 16x16 pixels or 32x32 pixels, using either 8-bit or 24-bit colors. The format of the image must be one of PNG (a W3C standard), GIF, or ICO.',
        verbose_name='Favicon',
        related_name='favicon')
    apple_touch_icon = models.ForeignKey(
        Image, models.SET_NULL, blank=True, null=True,
        verbose_name='Apple Touch Icon',
        help_text='The apple touch icon should be 114 x 114 or 144 x 144, and a png file.',
        related_name='touch_icon')
    show_breadcrumbs = models.BooleanField(
        default=False,
        verbose_name='Show Breadcrumbs',
        help_text='Check this box if you want breadcrumbs on this site.')

    # Progressive Web App Tab
    pwa_use_manifest = models.BooleanField(
        default=False,
        verbose_name='Use PWA Manifest',
        help_text='Check this box if you want to provide a PWA manifest.')
    pwa_short_name = models.TextField(
        null=True, blank=True, default='',
        verbose_name='Short Name',
        help_text='The short name of the site.')
    pwa_name = models.TextField(
        null=True, blank=True, default='',
        verbose_name='Name',
        help_text='The full name of the site.')

    pwa_icon_small = models.ForeignKey(
        Image, models.SET_NULL, blank=True, null=True,
        help_text='This icon should be a 192x192 pixel png file',
        verbose_name='Small Icon',
        related_name='pwa_small_icon')
    pwa_icon_large = models.ForeignKey(
        Image, models.SET_NULL, blank=True, null=True,
        verbose_name='Large Icon',
        help_text='This icon should be a 512x512 pixel png file',
        related_name='pwa_large_icon')
    pwa_start_url = models.TextField(
        null=True, blank=True, default='',
        verbose_name='Start URL',
        help_text='The relative path from which the app should start when opened.')
    pwa_background_color = models.TextField(
        null=True, blank=True, default='',
        verbose_name='Background Color',
        help_text='The overall background color of the app.')
    pwa_orientation = models.CharField(
        choices=(('user-selected', 'user-selected'), ('portrait', 'portrait'), ('landscape', 'landscape'),),
        default='user-selected',
        max_length=16,
        verbose_name='Display',
        help_text='Orientation of the app (generally should be left to user selected).')
    pwa_display = models.CharField(
        choices=(('fullscreen', 'fullscreen'), ('standalone', 'standalone'), ('browser', 'browser'),),
        default='standalone',
        max_length=16,
        verbose_name='Display',
        help_text='Display type for the app')
    pwa_scope = models.TextField(
        null=True, blank=True, default='',
        verbose_name='Scope',
        help_text='The scope of the app. In most cases should be root of the site. Start URL must be in the scope.')
    pwa_theme_color = models.TextField(
        null=True, blank=True, default='',
        verbose_name='Theme Color',
        help_text='The theme_color sets the color of the tool bar, and may be reflected in the app&rsquo;s preview in task switchers.')

    seo_tab_panels = [
        MultiFieldPanel([
            FieldPanel('google_analytics_tag'),
        ], heading='Analytics', classname='collapsible'),
    ]
    config_tab_panels = [
        MultiFieldPanel([
            ImageChooserPanel('favicon_ico'),
            ImageChooserPanel('apple_touch_icon'),
            FieldPanel('show_breadcrumbs'),
            FieldPanel('robots_txt'),
        ], heading='Configuration', classname='collapsible'),
    ]

    pwa_tab_panels = [
        MultiFieldPanel([
            FieldPanel('pwa_use_manifest'),
            FieldPanel('pwa_short_name'),
            FieldPanel('pwa_name'),
            ImageChooserPanel('pwa_icon_small'),
            ImageChooserPanel('pwa_icon_large'),
            FieldPanel('pwa_start_url'),
            FieldPanel('pwa_background_color'),
            FieldPanel('pwa_orientation'),
            FieldPanel('pwa_display'),
            FieldPanel('pwa_scope'),
            FieldPanel('pwa_theme_color'),
        ], heading='PWA Configuration', classname='collapsible'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(seo_tab_panels, heading='SEO & Analytics'),
        ObjectList(config_tab_panels, heading='Settings'),
        ObjectList(pwa_tab_panels, heading='PWA Settings'),
    ])

    class Meta:
        verbose_name = 'Site Settings'
