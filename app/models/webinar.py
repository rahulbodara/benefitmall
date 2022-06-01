from __future__ import unicode_literals
import datetime

from django import forms
from django.db import models

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.documents.edit_handlers import DocumentChooserPanel
from app.widgets import CustomRadioSelect
from app.models import DefaultPage
from site_settings.models import AbstractBasePage


class WebinarIndexPage(DefaultPage):
    subpage_types = ['app.WebinarPage']

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        StreamFieldPanel('body_below'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        AbstractBasePage.meta_panels,
    ])

    def serve(self, request, *args, **kwargs):
        webinar = WebinarPage.objects.all().order_by('-date')
        paginator = Paginator(webinar, 12)
        try:
            self.webinar = paginator.page(request.GET.get('page'))  # Return linked page
        except PageNotAnInteger:
            self.webinar = paginator.page(1)  # Return first page
        except EmptyPage:
            self.webinar = paginator.page(paginator.num_pages)  # Return last page

        return Page.serve(self, request, *args, **kwargs)

    @classmethod
    def can_create_at(cls, parent):
        # Only allow one child instance
        return super(WebinarIndexPage, cls).can_create_at(parent) and not cls.objects.exists()


class WebinarPage(DefaultPage):
    date = models.DateTimeField(default=datetime.datetime.today, help_text='Date displayed to the public, not related to scheduled publishing dates')
    image = models.ForeignKey('wagtailimages.Image', verbose_name='Image', null=True, on_delete=models.SET_NULL, related_name='+', help_text='Image Dimensions 200x230px')
    description = models.CharField(max_length=150, help_text='Short description of the webinar limited to 150 characters', null=True, blank=True)
    parent_page_types = ['WebinarIndexPage']

    content_panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            ImageChooserPanel('image'),
            FieldPanel('date'),
            FieldPanel('description', widget=forms.Textarea),
        ], heading='Info', classname='collapsible webinar-info'),
        StreamFieldPanel('body')
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        AbstractBasePage.meta_panels,
    ])

    def get_index(self):
        return self.get_parent().get_full_url()
