from __future__ import unicode_literals
import datetime

from datetime import date

from django import forms
from django.db import models
from django.http import Http404
from django.utils.dateformat import DateFormat
from django.utils.formats import date_format
from django.utils.html import format_html, strip_tags
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, TabbedInterface, ObjectList
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.fields import RichTextField
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from site_settings.models import AbstractBasePage

from modelcluster.fields import ParentalManyToManyField

from app.widgets import CustomRadioSelect
from .pages import DefaultPage


class BlogIndexPage(RoutablePageMixin, DefaultPage):
    PAGINATION_CHOICES = (
        (1, '1'),
        (2, '2'),
        (3, '3'),
        (4, '4'),
        (5, '5'),
        (6, '6'),
        (7, '7'),
        (8, '8'),
        (9, '9'),
        (10, '10'),
    )
    pagination = models.IntegerField(default=5, choices=PAGINATION_CHOICES, help_text='Choose how many posts appear per page')

    content_panels = DefaultPage.content_panels + [
        MultiFieldPanel([
            FieldPanel('pagination'),
        ], heading='Settings')
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        AbstractBasePage.meta_panels,
    ])

    subpage_types = ['BlogPage']

    class Meta:
        verbose_name = 'Blog Index Page'
        verbose_name_plural = 'Blog Index Pages'

    @classmethod
    def can_create_at(cls, parent):
        # Only allow one child instance
        return super(BlogIndexPage, cls).can_create_at(parent) and not cls.objects.child_of(parent).exists()

    def get_context(self, request, *args, **kwargs):
        context = super(BlogIndexPage, self).get_context(request, *args, **kwargs)
        context['posts'] = self.posts
        context['search_type'] = getattr(self, 'search_type', '')
        context['search_term'] = getattr(self, 'search_term', '')

        paginator = Paginator(self.posts, self.pagination)
        page = request.GET.get('page')
        try:
            paginated_posts = paginator.page(page)
        except PageNotAnInteger:
            paginated_posts = paginator.page(1)
        except EmptyPage:
            paginated_posts = paginator.page(paginator.num_pages)
        context['paginated_posts'] = paginated_posts
        return context

    def get_posts(self):
        return BlogPage.objects.live().order_by('-date')

    def get_categories(self):
        return BlogCategory.objects.order_by('name')

    @route(r'^(\d{4})/$')
    @route(r'^(\d{4})/(\d{2})/$')
    @route(r'^(\d{4})/(\d{2})/(\d{2})/$')
    def post_by_date(self, request, year, month=None, day=None, *args, **kwargs):
        self.posts = self.get_posts().filter(date__year=year)
        self.search_type = 'date'
        self.search_term = year
        if month:
            self.posts = self.posts.filter(date__month=month)
            df = DateFormat(date(int(year), int(month), 1))
            self.search_term = df.format('F Y')
        if day:
            self.posts = self.posts.filter(date__day=day)
            self.search_term = date_format(date(int(year), int(month), int(day)))
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
    def post_by_date_slug(self, request, year, month, day, slug, *args, **kwargs):
        post_page = self.get_posts().filter(slug=slug).first()
        if not post_page:
            raise Http404
        return Page.serve(post_page, request, *args, **kwargs)

    @route(r'^category/(?P<category>[-\w]+)/$')
    def post_by_category(self, request, category, *args, **kwargs):
        self.search_type = 'category'
        self.search_term = category
        self.posts = self.get_posts().filter(categories__slug=category)
        print('POSTS:', self.posts)
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^$')
    def post_list(self, request, *args, **kwargs):
        self.posts = self.get_posts()
        return Page.serve(self, request, *args, **kwargs)

    @route(r'^search/$')
    def post_search(self, request, *args, **kwargs):
        search_query = request.GET.get('q', None)
        self.posts = self.get_posts()
        if search_query:
            self.posts = self.posts.filter(body__contains=search_query)
            self.search_term = search_query
            self.search_type = 'search'
        return Page.serve(self, request, *args, **kwargs)


class BlogPage(DefaultPage):
    VIDEO_SOURCE_CHOICES = (
        ('', 'None'),
        ('https://www.youtube.com/embed/', 'YouTube'),
        ('https://player.vimeo.com/video/', 'Vimeo'),
    )
    categories = ParentalManyToManyField('BlogCategory', blank=True, help_text=format_html('Manage categories using the <a href="/admin/snippets/app/blogcategory/">Snippets &raquo; Categories</a> option in the sidebar'))
    date = models.DateTimeField(default=datetime.datetime.today, help_text='Date displayed to the public, not related to scheduled publishing dates')
    image = models.ForeignKey('wagtailimages.Image', verbose_name='Header Image', null=True, on_delete=models.SET_NULL, related_name='+', help_text='Header image also used as thumbnail')
    video_source = models.CharField(verbose_name='Header Video Source', null=True, blank=True, max_length=50, choices=VIDEO_SOURCE_CHOICES, default='', help_text='The source of the hosted header video')
    video_id = models.CharField(verbose_name='Header Video ID', max_length=50, null=True, blank=True, help_text='The unique id from the selected source above. Should only consist of alphanumeric characters. Ex: 86036070')
    excerpt = models.CharField(max_length=1000, blank=True, help_text='A teaser description of the content limited to 1000 characters')
    content = RichTextField(features=['h2', 'h3', 'h4', 'h5', 'h6', 'bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link', 'image', 'embed'])

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('categories', classname='blog-categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel('date'),
            ImageChooserPanel('image'),
            FieldPanel('video_source', classname='blog-video-source', widget=forms.RadioSelect),
            FieldPanel('video_id'),
            FieldPanel('excerpt', widget=forms.Textarea),
        ], heading='Info', classname='collapsible'),
        FieldPanel('content', classname='full'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        AbstractBasePage.meta_panels,
    ])

    parent_page_types = ['BlogIndexPage']
    subpage_types = []

    @property
    def blog_landing_page(self):
        return self.get_parent().specific

    def clean(self):
        cleaned_data = super().clean()
        errors = {}
        if self.video_source and not self.video_id:
            errors['video_id'] = ErrorList(['This field is required.'])
        if len(errors) > 0:
            raise ValidationError(errors)
        if not self.excerpt:
            # Build excerpt from content
            excerpt = self.content
            # Strip tags and slice to 350 characters
            excerpt = strip_tags(excerpt)[:350]
            # Split by a max of 50 words
            excerpt = excerpt.split(' ', 50)
            # Join the first 49 words, add an ellipsis
            self.excerpt = ' '.join(excerpt[:49]) + '...'
        return cleaned_data

    def get_context(self, request, *args, **kwargs):
        context = super(BlogPage, self).get_context(request, *args, **kwargs)
        context['blog_landing_page'] = self.blog_landing_page
        context['post'] = self
        return context


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=255, help_text='Category display name')
    slug = models.SlugField(unique=True, max_length=80, help_text='Lowercase alphanumberic version of the display name used in URLs')

    panels = [
        MultiFieldPanel([
            FieldPanel('name'),
            FieldPanel('slug'),
        ], heading='Category'),
    ]

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'


