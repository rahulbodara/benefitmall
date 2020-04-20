from __future__ import unicode_literals
import datetime

from django import forms
from django.db import models
from django.http import Http404
from django.utils.html import format_html
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import redirect

from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, TabbedInterface, ObjectList, StreamFieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.core.models import Page
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.models import register_snippet

from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager
from taggit.models import TaggedItemBase

from site_settings.models import AbstractBasePage

from app.models import DefaultPage


class BlogIndexPage(RoutablePageMixin, DefaultPage):
    subpage_types = ['app.BlogPage']

    class Meta:
        verbose_name = 'Blog Index Page'
        verbose_name_plural = 'Blog Index Pages'

    @classmethod
    def can_create_at(cls, parent):
        # Only allow one child instance
        return super(BlogIndexPage, cls).can_create_at(parent) and not cls.objects.child_of(parent).exists()

    def get_categories(self):
        return BlogCategory.objects.order_by('name')

    def get_tags(self):
        return [tag.tag for tag in BlogTag.objects.order_by('tag__name')]

    @route(r'^$')
    @route(r'^(\d{4})/$')
    @route(r'^(\d{4})/(\d{2})/$')
    @route(r'^(\d{4})/(\d{2})/(\d{2})/$')
    def blogs_list(self, request, year=None, month=None, day=None, *args, **kwargs):
        blogs = BlogPage.objects.live().order_by('-date', '-last_published_at')

        # Handle category filter
        self.filter_category = request.GET.get('category', None)
        if self.filter_category:
            blog_category = BlogCategory.objects.filter(slug=self.filter_category).first()
            if blog_category:
                self.filter_category = blog_category
                blogs = blogs.filter(categories=self.filter_category)
            else:
                self.filter_category = None

        # Handle tag filter
        self.filter_tag = request.GET.get('tag', None)
        if self.filter_tag:
            blog_tag = BlogTag.objects.filter(tag__slug=self.filter_tag).first()
            if blog_tag:
                self.filter_tag = blog_tag.tag
                blogs = blogs.filter(tags=self.filter_tag)
            else:
                self.filter_tag = None

        # Handle date filter
        self.filter_date = None
        if year:
            blogs = blogs.filter(date__year=year)
            self.filter_date = datetime.datetime.today().replace(year=int(year), month=1, day=1)
        if month:
            blogs = blogs.filter(date__month=month)
            self.filter_date = self.filter_date.replace(month=int(month))
        if day:
            blogs = blogs.filter(date__day=day)
            self.filter_date = self.filter_date.replace(day=int(day))

        # Handle pagination
        paginator = Paginator(blogs, 12)
        try:
            # Return linked page
            self.blogs = paginator.page(request.GET.get('page'))
        except PageNotAnInteger:
            # Return first page
            self.blogs = paginator.page(1)
        except EmptyPage:
            # Return last page
            self.blogs = paginator.page(paginator.num_pages)

        return Page.serve(self, request, *args, **kwargs)

    @route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
    def blog_page_detail(self, request, year, month, day, slug, *args, **kwargs):
        blog_page = BlogPage.objects.live().filter(date__year=year, date__month=month, date__day=day, slug=slug).first()
        if not blog_page:
            raise Http404

        self.additional_breadcrumbs = [({'title': blog_page.title, 'url': blog_page.get_url()})]
        return Page.serve(blog_page, request, *args, **kwargs)


class BlogPage(RoutablePageMixin, DefaultPage):
    date = models.DateTimeField(default=datetime.datetime.today, help_text='Date displayed to the public, not related to scheduled publishing dates')
    image = models.ForeignKey('wagtailimages.Image', verbose_name='Image', null=True, on_delete=models.SET_NULL, related_name='+', help_text='Hero image also used as thumbnail')
    excerpt = models.CharField(max_length=1000, help_text='Short description of the content limited to 1000 characters')
    author = models.CharField(max_length=200, blank=True, null=True)
    categories = ParentalManyToManyField('BlogCategory', blank=True, help_text=format_html('Manage categories using the <a href="/admin/snippets/app/blogcategory/">Snippets &raquo; Categories</a> option in the sidebar'))
    tags = ClusterTaggableManager(through='BlogTag', blank=True)

    content_panels = Page.content_panels + [
        MultiFieldPanel([
            FieldPanel('date'),
            ImageChooserPanel('image'),
            FieldPanel('excerpt', widget=forms.Textarea),
            FieldPanel('author'),
            FieldPanel('categories', classname='blog-categories', widget=forms.CheckboxSelectMultiple),
            FieldPanel('tags'),
        ], heading='Info', classname='collapsible'),
        StreamFieldPanel('body'),
    ]

    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        AbstractBasePage.meta_panels,
    ])

    parent_page_types = ['BlogIndexPage']
    subpage_types = []

    @route(r'^$')
    def redirect_to_detail_view(self, request, *args, **kwargs):
        return redirect(self.get_url())

    @property
    def get_blog_index_page(self):
        return self.get_parent().specific

    def get_url(self):
        return '{}{}{}/'.format(self.get_blog_index_page.url, self.date.strftime('%Y/%m/%d/'), self.slug)

    def get_full_url(self, request=None):
        url_parts = self.get_url_parts(request=request)
        site_id, root_url, page_path = url_parts
        return root_url + self.get_url()


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


class BlogTag(TaggedItemBase):
    content_object = ParentalKey('BlogPage', on_delete=models.CASCADE, related_name='tagged_items')
