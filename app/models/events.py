import datetime
import pytz
from django.db import models
from django.forms import ModelForm
from django.http import HttpResponse
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface, FieldRowPanel
from app.models.pages import DefaultPage
from wagtail.core.models import Page, Http404, TemplateResponse
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.text import slugify
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from app.models.pages import AbstractBasePage
from app.widgets.event_detail_widget import EventDetailWidget


class EventIndexPage(RoutablePageMixin, DefaultPage):
	subpage_types = ['app.EventPage']

	@route(r'^$')
	@route(r'^(\d{4})/$')
	@route(r'^(\d{4})/(\d{2})/$')
	@route(r'^(\d{4})/(\d{2})/(\d{2})/$')
	def events_list(self, request, year=None, month=None, day=None, *args, **kwargs):
		context = super().get_context(request, **kwargs)
		self.additional_breadcrumbs = []

		all_events = EventPage.objects.all()
		if year:
			all_events = all_events.filter(start_datetime__year=year)
		if month:
			all_events = all_events.filter(start_datetime__month=month)
		if day:
			all_events = all_events.filter(start_datetime__day=day)

		paginator = Paginator(all_events, 10)

		try:
			# Return linked page
			events = paginator.page(request.GET.get('page'))
			print('======= LINKED PAGE')
		except PageNotAnInteger:
			# Return first page
			events = paginator.page(1)
			print('======= FIRST PAGE')
		except EmptyPage:
			# Return last page
			events = paginator.page(paginator.num_pages)
			print('======= LAST PAGE')

		context['events'] = events
		return TemplateResponse(request, self.get_template(request), context)

	@route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
	def event_detail(self, request, year, month, day, slug, *args, **kwargs):
		context = super().get_context(request, **kwargs)

		# Get event
		try:
			slug_items = slug.split('-')
			event = EventPage.objects.get(start_datetime__year=year, start_datetime__month=month, start_datetime__day=day, id=slug_items[-1])
			self.additional_breadcrumbs = [({'title':event.title, 'url': self.url+year+'/'+month+'/'+day+'/'+slug+'/'})]
		except Event.DoesNotExist:
			raise Http404

		registered = request.GET.get('registered', None)

		if request.method == 'POST' and event.is_active() and not registered:
			form = EventRegistrationForm(request.POST)
			if form.is_valid():
				form.save()
				cleaned_data = form.cleaned_data
				
				# Prepare registration email
				mail_message = ''
				for field, value in cleaned_data.items():
					if value:
						mail_message += '{}: {} <br>'.format(field.upper(), value)

				# Send registration email
				send_mail(
					subject='Event Registration',
					message=mail_message,
					html_message=mail_message,
					from_email='test@test.com',
					recipient_list=['phorn@insite.net'],
					fail_silently=False
				)
				return redirect('{}{}/{}/{}/{}/?registration=complete'.format(self.url, year, month, day, slug))
		else:
			form = EventRegistrationForm()

		context['form'] = form
		context['event'] = event
		context['registered'] = registered
		return TemplateResponse(request, "app/event_page.html", context)

	@classmethod
	def can_create_at(cls, parent):
		# Only allow one child instance
		return super(EventIndexPage, cls).can_create_at(parent) and not cls.objects.exists()


class EventPage(RoutablePageMixin, DefaultPage):
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

	content_panels = [
		MultiFieldPanel([
			FieldPanel('title'),
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
	]

    # Tabs
	edit_handler = TabbedInterface([
		ObjectList(content_panels, heading='Content'),
		AbstractBasePage.meta_panels,
	])

	parent_page_types = ['app.EventIndexPage']
	subpage_types = []

	class Meta:
		verbose_name = 'Event'
		verbose_name_plural = 'Events'
		ordering = ['start_datetime']

	@route(r'^$')
	def hide_default_view(self, request, *args, **kwargs):
		raise Http404

	@route(r'^calendar/$')
	def generate_ics(self, request, *args, **kwargs):
		# Method to reformat lines to specific length
		def reformat_lines(item):
			item = item[:61] + '\n ' + item[61:]
			item = '\n '.join(item[i:i + 74] for i in range(0, len(item), 74))
			return item

		location = 'Online' if self.location_type == 'online' else '{}{}{}{}{}'.format(
			self.address_line_1 if self.address_line_1 else '',
			' ' + self.address_line_2 if self.address_line_2 else '',
			' ' + self.city + ',' if self.city else '',
			' ' + self.state if self.state else '',
			' ' + self.postal_code if self.postal_code else '',
		)
		summary = self.title
		filename = 'Benefit_Mall_{}.ics'.format(self.title.replace(' ', '_'))
		start = self.start_datetime.strftime('%Y%m%dT%H%M%S')
		end = self.get_end_datetime().strftime('%Y%m%dT%H%M%S')
		now = datetime.datetime.now().strftime('%Y%m%dT%H%M%S')
		description = 'Event: {}'.format(self.title)
		description += '\\n\\nLocation Type:\\n{}'.format(self.location_type)
		# description += '\\n{}'.format(clinic.get_full_address(directions=False).replace('<br/>','\\n'))

		content = ''
		content += 'BEGIN:VCALENDAR\n'
		content += 'VERSION:2.0\n'
		content += 'PRODID:-//utswmed.org//Open Scheduling\n'
		content += 'CALSCALE:GREGORIAN\n'
		content += 'BEGIN:VTIMEZONE\n'
		content += 'TZID:America/Chicago\n'
		content += 'TZURL:http://tzurl.org/zoneinfo-outlook/America/Chicago\n'
		content += 'X-LIC-LOCATION:America/Chicago\n'
		content += 'BEGIN:DAYLIGHT\n'
		content += 'TZOFFSETFROM:-0600\n'
		content += 'TZOFFSETTO:-0500\n'
		content += 'TZNAME:CDT\n'
		content += 'DTSTART:19700308T020000\n'
		content += 'RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU\n'
		content += 'END:DAYLIGHT\n'
		content += 'BEGIN:STANDARD\n'
		content += 'TZOFFSETFROM:-0500\n'
		content += 'TZOFFSETTO:-0600\n'
		content += 'TZNAME:CST\n'
		content += 'DTSTART:19701101T020000\n'
		content += 'RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU\n'
		content += 'END:STANDARD\n'
		content += 'END:VTIMEZONE\n'
		content += 'BEGIN:VEVENT\n'
		content += 'DTSTAMP:{}\n'.format(now)
		content += 'UID:{}-{}@benefitmall.com\n'.format(now, hash(self.title))
		content += 'DTSTART;TZID=America/Chicago:{}\n'.format(start)
		content += 'DTEND;TZID=America/Chicago:{}\n'.format(end)
		content += 'SUMMARY:{}\n'.format(summary)
		content += 'DESCRIPTION:{}\n'.format(reformat_lines(description))
		content += 'LOCATION:{}\n'.format(reformat_lines(location))
		content += 'BEGIN:VALARM\n'
		content += 'ACTION:DISPLAY\n'
		content += 'DESCRIPTION:{}\n'.format(summary)
		content += 'TRIGGER:-PT1H\n'
		content += 'END:VALARM\n'
		content += 'END:VEVENT\n'
		content += 'END:VCALENDAR'

		response = HttpResponse(content, content_type='text/calendar')
		response['Content-Disposition'] = 'attachment; filename="{}"'.format(filename)
		return response

	def __str__(self):
		return self.title

	def get_url(self):
		return '{}{}{}/'.format(self.get_parent().url, self.start_datetime.strftime('%Y/%m/%d/'), slugify(self.title + ' ' + str(self.id)))

	def get_end_datetime(self):
		hours, minutes = str(self.duration).split('.')
		return self.start_datetime + datetime.timedelta(hours=int(hours), minutes=int(minutes)/100 * 60)
		
	def is_active(self):
		central_timezone = pytz.timezone('America/Chicago')
		return self.get_end_datetime().replace(tzinfo=central_timezone) > datetime.datetime.now().replace(tzinfo=central_timezone)


class EventRegistration(models.Model):
	event = models.ForeignKey(EventPage, on_delete=models.PROTECT, null=True, blank=True, related_name='registered_event')
	created_at = models.DateTimeField(auto_now_add=True)
	first_name = models.CharField(max_length=255, default='', verbose_name='First Name')
	last_name = models.CharField(max_length=255, default='', verbose_name='Last Name')
	company = models.CharField(max_length=255, default='', verbose_name='Company')
	email = models.EmailField()
	phone = models.CharField(max_length=16, default='', verbose_name='Phone')
	address1 = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name='Address Line 1')
	address2 = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name='Address Line 2')
	city = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name='City')
	state = models.CharField(max_length=16, default='', null=True, blank=True, verbose_name='State')
	postalcode = models.CharField(max_length=16, default='', verbose_name='Postal Code')

	def __str__(self):
		return "Registration: {} - {}".format(self.event.title, self.created_at)

	panels = [
		FieldPanel('event', widget=EventDetailWidget),
		MultiFieldPanel([
			FieldPanel('first_name'),
			FieldPanel('last_name'),
			FieldPanel('company'),
			FieldPanel('email'),
			FieldPanel('phone'),
			FieldPanel('address1'),
			FieldPanel('address2'),
			FieldPanel('city'),
			FieldPanel('state'),
			FieldPanel('postalcode'),
		], heading="Registration"),
	]


class EventRegistrationForm(ModelForm):

	class Meta:
		model = EventRegistration
		exclude = ['created']
