from django.db import models
from django.shortcuts import redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.core.models import Page, Http404
from wagtail.admin.edit_handlers import MultiFieldPanel, FieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from app.models.pages import DefaultPage, AbstractBasePage


class NewsIndexPage(RoutablePageMixin, DefaultPage):
	subpage_types = ['app.NewsPage']

	class Meta:
		verbose_name = 'News Index Page'
		verbose_name_plural = 'News Index Pages'

	@route(r'^$')
	@route(r'^(\d{4})/$')
	@route(r'^(\d{4})/(\d{2})/$')
	@route(r'^(\d{4})/(\d{2})/(\d{2})/$')
	def news_list(self, request, year=None, month=None, day=None, *args, **kwargs):
		all_news = NewsPage.objects.all().order_by('-news_datetime')
		if year:
			all_news = all_news.filter(news_datetime__year=year)
		if month:
			all_news = all_news.filter(news_datetime__month=month)
		if day:
			all_news = all_news.filter(news_datetime__day=day)

		paginator = Paginator(all_news, 10)
		try:
			news = paginator.page(request.GET.get('page'))  # Return linked page
		except PageNotAnInteger:
			news = paginator.page(1)  # Return first page
		except EmptyPage:
			news = paginator.page(paginator.num_pages)  # Return last page

		self.news = news
		self.additional_breadcrumbs = []
		return Page.serve(self, request, *args, **kwargs)

	@route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
	def news_page_detail(self, request, year, month, day, slug, *args, **kwargs):
		try:
			news_page = NewsPage.objects.get(news_datetime__year=year, news_datetime__month=month, news_datetime__day=day, slug=slug)
		except NewsPage.DoesNotExist:
			raise Http404

		news_page.additional_breadcrumbs = [({'title': news_page.title, 'url': news_page.get_url()})]
		return Page.serve(news_page, request, *args, **kwargs)

	@classmethod
	def can_create_at(cls, parent):
		# Only allow one child instance
		return super(NewsIndexPage, cls).can_create_at(parent) and not cls.objects.exists()


class NewsPage(RoutablePageMixin, DefaultPage):
	news_datetime = models.DateTimeField(verbose_name='Date & Time', help_text="The date and time of the press release.")
	image = models.ForeignKey('wagtailimages.Image', verbose_name='Image', null=True, on_delete=models.SET_NULL, related_name='+', help_text='Recommended size: 350 W x 220 H')

	content_panels = Page.content_panels + [
		MultiFieldPanel([
			FieldPanel('news_datetime'),
			ImageChooserPanel('image'),
		], heading="Event"),
		StreamFieldPanel('body'),
	]

	# Tabs
	edit_handler = TabbedInterface([
		ObjectList(content_panels, heading='Content'),
		AbstractBasePage.meta_panels,
	])

	parent_page_types = ['app.NewsIndexPage']
	subpage_types = []

	class Meta:
		verbose_name = 'Press Release'
		verbose_name_plural = 'Press Releases'
		ordering = ['news_datetime']

	@route(r'^$')
	def redirect_to_detail_view(self, request, *args, **kwargs):
		return redirect(self.get_url())

	def __str__(self):
		return self.title

	def get_url(self):
		return '{}{}{}/'.format(self.get_parent().url, self.news_datetime.strftime('%Y/%m/%d/'), self.slug)

	def get_full_url(self, request=None):
		url_parts = self.get_url_parts(request=request)
		site_id, root_url, page_path = url_parts
		return root_url + self.get_url()
