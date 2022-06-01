from __future__ import unicode_literals
import datetime

from django import forms
from django.db import models

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, StreamFieldPanel, TabbedInterface, ObjectList
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel

from app.models import DefaultPage
from site_settings.models import AbstractBasePage


class PodcastIndexPage(DefaultPage):
    subpage_types = []

    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
        StreamFieldPanel('body_below'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        AbstractBasePage.meta_panels,
    ])

    def serve(self, request, *args, **kwargs):
        podcast = Podcast.objects.all().order_by('-date')
        paginator = Paginator(podcast, 12)
        try:
            self.podcast = paginator.page(request.GET.get('page'))  # Return linked page
        except PageNotAnInteger:
            self.podcast = paginator.page(1)  # Return first page
        except EmptyPage:
            self.podcast = paginator.page(paginator.num_pages)  # Return last page

        return Page.serve(self, request, *args, **kwargs)

    @classmethod
    def can_create_at(cls, parent):
        # Only allow one child instance
        return super(PodcastIndexPage, cls).can_create_at(parent) and not cls.objects.exists()


class Podcast(models.Model):
    date = models.DateTimeField(default=datetime.datetime.today, help_text='Date displayed to the public, not related to scheduled publishing dates')
    image = models.ForeignKey('wagtailimages.Image', verbose_name='Image', null=True, on_delete=models.SET_NULL, related_name='+', help_text='Image Dimensions 200x230px')
    title = models.CharField(max_length=150, help_text='Podcast Title')
    description = models.CharField(max_length=150, help_text='Short description of the podcast limited to 150 characters')
    link = models.URLField(help_text='Link to Podcast')

    panels = [
        MultiFieldPanel([
            FieldPanel('title'),
            ImageChooserPanel('image'),
            FieldPanel('link'),
            FieldPanel('date'),
            FieldPanel('description', widget=forms.Textarea),
        ], heading='Info', classname='collapsible'),
    ]

    def get_index(self):
        return PodcastIndexPage.objects.first().get_full_url()