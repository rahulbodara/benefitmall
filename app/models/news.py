from django.db import models
from django.forms import ModelForm
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface, FieldRowPanel
from app.models.pages import DefaultPage
from wagtail.core.models import Page, Http404, TemplateResponse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from wagtail.contrib.routable_page.models import RoutablePageMixin, route


class NewsIndexPage(RoutablePageMixin, DefaultPage):
	template = "app/news_index_page.html"
	@route(r'^$')
	@route(r'^(\d{4})/$')
	@route(r'^(\d{4})/(\d{2})/$')
	@route(r'^(\d{4})/(\d{2})/(\d{2})/$')
	def posts_by_date(self, request, year=None, month=None, day=None, *args, **kwargs):
		context = super().get_context(request, **kwargs)
		self.additional_breadcrumbs = []
		if year and month and day:
			articles = News.objects.filter(news_datetime__year=year, news_datetime__month=month, news_datetime__day=day)
			# self.additional_breadcrumbs.append({'title':year, 'url': '/news-press/'+year+'/'})
			# self.additional_breadcrumbs.append({'title':month, 'url': '/news-press/'+year+'/'+month+'/'})
			# self.additional_breadcrumbs.append({'title':day, 'url': '/news-press/'+year+'/'+month+'/'+day+'/'})

		elif year and month:
			articles = News.objects.filter(news_datetime__year=year, news_datetime__month=month)
			# self.additional_breadcrumbs.append({'title':year, 'url': '/news-press/'+year+'/'})
			# self.additional_breadcrumbs.append({'title':month, 'url': '/news-press/'+year+'/'+month+'/'})
		elif year:
			articles = News.objects.filter(news_datetime__year=year)
			# self.additional_breadcrumbs.append({'title':year, 'url': '/news-press/'+year+'/'})
		else:
			articles = News.objects.all()
		context['articles'] = articles
		return TemplateResponse(request, "app/news_index_page.html", context)

	@route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
	def post_by_date_slug(self, request, year, month, day, slug, *args, **kwargs):
		context = super().get_context(request, **kwargs)
		self.additional_breadcrumbs = []
		try:
			article = News.objects.get(news_datetime__year=year, news_datetime__month=month, news_datetime__day=day, news_slug=slug)
			# self.additional_breadcrumbs.append({'title':year, 'url': '/news-press/'+year+'/'})
			# self.additional_breadcrumbs.append({'title':month, 'url': '/news-press/'+year+'/'+month+'/'})
			# self.additional_breadcrumbs.append({'title':day, 'url': '/news-press/'+year+'/'+month+'/'+day+'/'})
			self.additional_breadcrumbs.append({'title':article.news_title, 'url': '/news-press/'+year+'/'+month+'/'+day+'/'+slug+'/'})
		except News.DoesNotExist:
			raise Http404

		context['article'] = article
		if not article:
			raise Http404
		return TemplateResponse(request, "app/news_detail_page.html", context)

	@classmethod
	def can_create_at(cls, parent):
		# Only allow one child instance
		return super(NewsIndexPage, cls).can_create_at(parent) and not cls.objects.exists()


class News(models.Model):
	news_slug = models.SlugField(max_length=255, verbose_name='URL Name', null=True, blank=True)
	news_title = models.CharField(max_length=255, verbose_name='Title')
	news_datetime = models.DateTimeField(verbose_name='Date & Time', help_text="The date and time of the press release.")
	body = RichTextField(default='', verbose_name='Body')

	panels = [
		MultiFieldPanel([
			FieldPanel('news_title'),
			FieldPanel('news_datetime'),
			FieldPanel('body'),
		], heading="Press Release"),
		MultiFieldPanel([
			FieldPanel('news_slug'),
		], heading="URL", classname='collapsible collapsed'),

	]

	def __str__(self):
		return self.news_title

	class Meta:
		ordering = ['news_datetime']


@receiver(pre_save, sender=News)
def my_handler(sender, instance=None, raw=False, **kwargs):
	news = instance
	if not news.news_slug:
		slug_str = "%s %s" % (news.news_title, news.pk)
		slug = slugify(slug_str)
		news.news_slug = slug
