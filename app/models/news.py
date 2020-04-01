from django.db import models
from django.apps import apps
from django.forms import ModelForm
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface, FieldRowPanel
from app.models.pages import DefaultPage, AbstractBasePage
from wagtail.core.models import Page, Http404, TemplateResponse
from wagtail.search import index
from django.dispatch import receiver
from django.shortcuts import redirect
from django.utils.text import slugify
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from site_settings.views import get_page_meta_data


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
		context = super().get_context(request, **kwargs)
		self.additional_breadcrumbs = []

		all_news = NewsPage.objects.all()
		if year:
			all_news = all_news.filter(news_datetime__year=year)
		if month:
			all_news = all_news.filter(news_datetime__month=month)
		if day:
			all_news = all_news.filter(news_datetime__day=day)

		featured_news = None
		news = None
		if all_news.count() > 0:
			featured_news = all_news[0]
			news = all_news[1:]

			paginator = Paginator(news, 10)

			try:
				# Return linked page
				news = paginator.page(request.GET.get('page'))
			except PageNotAnInteger:
				# Return first page
				news = paginator.page(1)
			except EmptyPage:
				# Return last page
				news = paginator.page(paginator.num_pages)

		HeaderFooter = apps.get_model(app_label='app', model_name='HeaderFooter')
		header_footer = HeaderFooter.for_site(site=request.site)
		context['featured_news_bg'] = header_footer.featured_news_bg
		context['featured_news'] = featured_news
		context['news'] = news
		return TemplateResponse(request, self.get_template(request), context)

	@route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
	def news_page_detail(self, request, year, month, day, slug, *args, **kwargs):
		context = super().get_context(request, **kwargs)

		# Get news item
		try:
			slug_items = slug.split('-')
			news_page = NewsPage.objects.get(news_datetime__year=year, news_datetime__month=month, news_datetime__day=day, id=slug_items[-1])
			self.additional_breadcrumbs = [({'title':news_page.title, 'url': news_page.get_url()})]
		except NewsPage.DoesNotExist:
			raise Http404

		context['page'] = news_page
		context.update(get_page_meta_data(request, news_page))
		return TemplateResponse(request, "app/news_page.html", context)

	@classmethod
	def can_create_at(cls, parent):
		# Only allow one child instance
		return super(NewsIndexPage, cls).can_create_at(parent) and not cls.objects.exists()


class NewsPage(RoutablePageMixin, DefaultPage):
	news_datetime = models.DateTimeField(verbose_name='Date & Time', help_text="The date and time of the press release.")

	content_panels = Page.content_panels + [
		FieldPanel('news_datetime'),
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
		return '{}{}{}/'.format(self.get_parent().url, self.news_datetime.strftime('%Y/%m/%d/'), slugify(self.title + ' ' + str(self.id)))

	def get_full_url(self, request=None):
		url_parts = self.get_url_parts(request=request)
		site_id, root_url, page_path = url_parts
		return root_url + self.get_url()
