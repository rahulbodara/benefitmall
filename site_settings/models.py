from django.db import models
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.images.models import Image
from wagtail.admin.edit_handlers import (
    FieldPanel, FieldRowPanel,
    InlinePanel, MultiFieldPanel,
    StreamFieldPanel, TabbedInterface,
    ObjectList, PageChooserPanel
)
from wagtail.core.fields import RichTextField, StreamField
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.search import index

from .views import get_page_meta_data


class AbstractBasePage(Page):
    # Hide from sitemap
    hide_in_sitemap = models.BooleanField(default=False, verbose_name="Hide in sitemap",
                                          help_text="Don't show this page in the sitemap.")
    # Add Contact Form
    include_contact_form = models.BooleanField(default=False, verbose_name="Attach Contact Form",
                                               help_text="Attach Contact Form To Bottom of Page")
    # SEO Metadata Fields
    canonical_url = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="Canonical URL",
        help_text='Leave this blank unless you know there is a canonical URL for this content.')
    meta_keywords = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="Meta Keywords")
    og_title = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="OG:Title")
    og_type = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="OG:Type")
    og_url = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="OG:URL")
    og_image = models.ForeignKey(
        Image, blank=True, null=True,
        verbose_name="OG:Image",
        related_name="page_og_image", on_delete=models.SET_NULL)
    og_description = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="OG:Description")

    # Meta Tab
    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldRowPanel([
                FieldPanel('show_in_menus'),
                FieldPanel('hide_in_sitemap'),
                FieldPanel('include_contact_form'),
            ]),
            FieldPanel('canonical_url'),
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
            FieldPanel('meta_keywords'),
        ], heading='Meta Information', classname='collapsible'),
        MultiFieldPanel([
            FieldPanel('og_title'),
            FieldPanel('og_type'),
            FieldPanel('og_url'),
            ImageChooserPanel('og_image'),
            FieldPanel('og_description'),
        ], heading='Open Graph Information', classname='collapsible'),
    ]
    # Add in publish dates
    meta_panels = ObjectList(promote_panels + Page.settings_panels, heading='Meta', classname='settings')

    search_fields = Page.search_fields + [
        index.SearchField('search_description'),
        index.SearchField('meta_keywords'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context.update(get_page_meta_data(request, self))
        return context

    class Meta:
        abstract = True


class AbstractBaseEmailForm(AbstractEmailForm):
    # Hide from sitemap
    hide_in_sitemap = models.BooleanField(default=False, verbose_name="Hide this page from the sitemap?")
    # Add Contact Form
    include_contact_form = models.BooleanField(default=False, verbose_name="Attach Contact Form",
                                               help_text="Attach Contact Form To Bottom of Page")
    # SEO Metadata Fields
    canonical_url = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="Canonical URL",
        help_text='Leave this blank unless you know there is a canonical URL for this content.')
    meta_keywords = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="Meta Keywords")
    og_title = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="OG:Title")
    og_type = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="OG:Type")
    og_url = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="OG:URL")
    og_image = models.ForeignKey(
        Image, blank=True, null=True,
        verbose_name="OG:Image",
        related_name="form_og_image", on_delete=models.SET_NULL)
    og_description = models.CharField(
        max_length=255, blank=True, null=True,
        verbose_name="OG:Description")

    # Meta Tab
    promote_panels = [
        MultiFieldPanel([
            FieldPanel('slug'),
            FieldRowPanel([
                FieldPanel('show_in_menus'),
                FieldPanel('hide_in_sitemap'),
                FieldPanel('include_contact_form')
            ]),
            FieldPanel('canonical_url'),
            FieldPanel('seo_title'),
            FieldPanel('search_description'),
            FieldPanel('meta_keywords'),
        ], heading='Meta Information', classname='collapsible'),
        MultiFieldPanel([
            FieldPanel('og_title'),
            FieldPanel('og_type'),
            FieldPanel('og_url'),
            ImageChooserPanel('og_image'),
            FieldPanel('og_description'),
        ], heading='Open Graph Information', classname='collapsible'),
    ]
    # Add in publish dates
    meta_panels = ObjectList(promote_panels + Page.settings_panels, heading='Meta', classname='settings')

    search_fields = Page.search_fields + [
        index.SearchField('search_description'),
        index.SearchField('meta_keywords'),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request)
        context.update(get_page_meta_data(request, self))
        return context

    class Meta:
        abstract = True