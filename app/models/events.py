from django.db import models
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface, FieldRowPanel
from app.models.pages import DefaultPage
from wagtail.core.models import Page, Http404, TemplateResponse
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils.text import slugify

from wagtail.contrib.routable_page.models import RoutablePageMixin, route


class EventIndexPage(RoutablePageMixin, DefaultPage):
	template = "app/event_index_page.html"

	@route(r'^$')
	@route(r'^(\d{4})/$')
	@route(r'^(\d{4})/(\d{2})/$')
	@route(r'^(\d{4})/(\d{2})/(\d{2})/$')
	def posts_by_date(self, request, year=None, month=None, day=None, *args, **kwargs):
		context = super().get_context(request, **kwargs)
		if year and month and day:
			events = Event.objects.filter(start_datetime__year=year, start_datetime__month=month, start_datetime__day=day)
		elif year and month:
			events = Event.objects.filter(start_datetime__year=year, start_datetime__month=month)
		elif year:
			events = Event.objects.filter(start_datetime__year=year)
		else:
			events = Event.objects.all()
		context['events'] = events
		return TemplateResponse(request, "app/event_index_page.html", context)

	@route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
	def post_by_date_slug(self, request, year, month, day, slug, *args, **kwargs):
		context = super().get_context(request, **kwargs)
		try:
			event = Event.objects.get(start_datetime__year=year, start_datetime__month=month, start_datetime__day=day, event_slug=slug)
		except Event.DoesNotExist:
			raise Http404

		context['event'] = event
		if not event:
			raise Http404
		return TemplateResponse(request, "app/event_detail_page.html", context)

	@classmethod
	def can_create_at(cls, parent):
		# Only allow one child instance
		return super(EventIndexPage, cls).can_create_at(parent) and not cls.objects.exists()

class Event(models.Model):
	LOCATION_TYPE_CHOICES = (
		('online', 'Online'),
		('in_person', 'In Person'),
	)
	TYPE_CHOICES = (
		('Benefits Meeting', 'Benefits Meeting'),
		('Benefits Training', 'Benefits Training'),
		('Compliance Webcast', 'Compliance Webcast'),
		('Tradeshow', 'Tradeshow'),
	)
	event_slug = models.SlugField(max_length=255, verbose_name='URL Name', null=True, blank=True)

	event_title = models.CharField(max_length=255, verbose_name='Title')
	event_type = models.CharField(max_length=24, choices=TYPE_CHOICES, default='', verbose_name='Event Type')
	description = RichTextField(default='', verbose_name='Description')

	location_type = models.CharField(max_length=24, choices=LOCATION_TYPE_CHOICES, default='', verbose_name='Location Type', help_text="If online, no address is necessary")
	address_line_1 = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name='Address Line 1')
	address_line_2 = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name='Address Line 2')
	address_city = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name='City')
	address_state = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name='State')
	address_zipcode = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name='Postal Code')

	start_datetime = models.DateTimeField(verbose_name='Date & Time', help_text="The date and time the event starts.")
	duration = models.DecimalField(decimal_places=2, max_digits=4, default=1, null=True, blank=True, help_text="In hours", verbose_name='Duration')

	cost = models.CharField(max_length=50, default='Free', help_text="If adding a price, please use the currency symbol, e.g. $, £, etc.")


	panels = [
		MultiFieldPanel([
			FieldPanel('event_title'),
			FieldRowPanel([
				FieldPanel('event_type'),
				FieldPanel('cost'),
			]),
			FieldRowPanel([
				FieldPanel('start_datetime'),
				FieldPanel('duration'),
			]),
			FieldPanel('description'),
		], heading="Event"),
		MultiFieldPanel([
			FieldPanel('location_type'),
			FieldPanel('address_line_1'),
			FieldPanel('address_line_2'),
			FieldPanel('address_city'),
			FieldPanel('address_state'),
			FieldPanel('address_zipcode'),
		], heading="Location", classname='collapsible'),
		MultiFieldPanel([
			FieldPanel('event_slug'),
		], heading="URL", classname='collapsible collapsed'),

	]

	def __str__(self):
		return self.event_title

	class Meta:
		ordering = ['start_datetime']


@receiver(pre_save, sender=Event)
def my_handler(sender, instance=None, raw=False, **kwargs):
	event = instance
	if not event.event_slug:
		slug_str = "%s %s" % (event.event_title, event.pk)
		slug = slugify(slug_str)
		event.event_slug = slug
