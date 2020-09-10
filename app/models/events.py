import datetime
import pytz
import html
import re

from django.conf import settings
from django.db import models
from django.forms import ModelForm
from django.http import HttpResponse
from django.shortcuts import redirect
from django.core.mail import send_mail
from django.forms.utils import ErrorList
from django.core.exceptions import ValidationError
from django.utils.html import strip_tags, format_html
from django.template.loader import render_to_string

from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface, FieldRowPanel
from wagtail.core.models import Page, Http404
from wagtail.search import index
from wagtail.snippets.models import register_snippet
from wagtail.admin.widgets import AdminTagWidget
from wagtail.contrib.routable_page.models import RoutablePageMixin, route
from wagtail.images.edit_handlers import ImageChooserPanel

from app.models import DefaultPage, AbstractBasePage
from app.widgets.event_detail_widget import EventDetailWidget
from app.choices.model_choices import EVENT_LOCATION_TYPE_CHOICES


class EventIndexPage(RoutablePageMixin, DefaultPage):
	email_enabled_global = models.BooleanField(verbose_name='Send Registration Emails', default=False, help_text='Check to enable sending registration emails. This is the default global setting for all events, but can be individually configured per event.')
	email_recipients_global = models.CharField(verbose_name='Email Recipients', max_length=200, blank=True, null=True, help_text='Add registration email recipients separated by commas. This is the default global setting for all events.')

	content_panels = Page.content_panels + [
		MultiFieldPanel([
			FieldPanel('email_enabled_global'),
			FieldPanel('email_recipients_global', widget=AdminTagWidget),
		], heading='Global Email Settings', classname='collapsible collapsed'),
		StreamFieldPanel('body'),
		StreamFieldPanel('body_below'),
	]

	# Tabs
	edit_handler = TabbedInterface([
		ObjectList(content_panels, heading='Content'),
		AbstractBasePage.meta_panels,
	])

	subpage_types = ['app.EventPage']
	additional_breadcrumbs = []

	@route(r'^$')
	@route(r'^(\d{4})/$')
	@route(r'^(\d{4})/(\d{2})/$')
	@route(r'^(\d{4})/(\d{2})/(\d{2})/$')
	def events_list(self, request, year=None, month=None, day=None, *args, **kwargs):
		self.additional_breadcrumbs = []
		self.year = year
		self.month = month
		self.day = day
		self.archive = False
		return Page.serve(self, request, *args, **kwargs)

	@route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
	def event_detail(self, request, year, month, day, slug, *args, **kwargs):
		try:
			event = EventPage.objects.live().get(start_datetime__year=year, start_datetime__month=month, start_datetime__day=day, slug=slug)
		except EventPage.DoesNotExist:
			raise Http404

		if not event.is_active():
			return redirect(event.get_url())

		registered = request.GET.get('registered', None)

		if request.method == 'POST' and event.is_active() and not registered:
			form = EventRegistrationForm(request.POST)
			if form.is_valid():
				form.save()

				# SEND ADMIN EMAIL
				if event.email_setting == 'enabled' or (event.email_setting == '' and self.email_enabled_global):

					# Get recipients
					if event.email_recipients:
						recipients = event.email_recipients
					else:
						recipients = self.email_recipients_global

					# Prepare message
					mail_message = ''
					for field, value in form.cleaned_data.items():
						if value:
							mail_message += '{}: {} \n'.format(field.upper(), value)

					# Send email
					send_mail(
						subject='Event Registration',
						message=mail_message,
						html_message=mail_message.replace('\n', '<br>'),
						from_email='www_no-reply@benefitmall.com',
						recipient_list=recipients.split(','),
						fail_silently=False
					)

				context = {
					'event': event,
					'first_name': form.cleaned_data['first_name'],
					'last_name': form.cleaned_data['last_name'],
				}

				# SEND CONFIRMATION EMAIL
				message_plain = render_to_string('emails/event_registration_confirmation.txt', context)
				message_html = render_to_string('emails/event_registration_confirmation.html', context)

				# Send email
				send_mail(
					subject='Registration Confirmation: ' + event.title,
					message=message_plain,
					html_message=message_html,
					from_email='www_no-reply@benefitmall.com',
					recipient_list=[form.cleaned_data['email']],
					fail_silently=False
				)

				return redirect('{}{}/{}/{}/{}/?registered=yes'.format(self.url, year, month, day, slug))
		else:
			form = EventRegistrationForm()

		event.additional_breadcrumbs = [({'title': event.title, 'url': event.get_url()})]
		event.form = form
		event.registered = registered
		return Page.serve(event, request, *args, **kwargs)

	def get_archive_page(self):
		return EventArchiveIndexPage.objects.live().first()

	def clean(self):
		super().clean()
		errors = {}
		if self.email_enabled_global and not self.email_recipients_global:
			errors['email_recipients_global'] = ErrorList(['Email Recipients is required when Send Registration Emails is enabled'])
		if len(errors) > 0:
			raise ValidationError(errors)

	@classmethod
	def can_create_at(cls, parent):
		# Only allow one instance
		return super().can_create_at(parent) and not cls.objects.exists()

	class Meta:
		verbose_name = 'Event Index Page'
		verbose_name_plural = 'Event Index Pages'


class EventArchiveIndexPage(RoutablePageMixin, DefaultPage):
	subpage_types = []
	additional_breadcrumbs = []

	@route(r'^$')
	@route(r'^(\d{4})/$')
	@route(r'^(\d{4})/(\d{2})/$')
	@route(r'^(\d{4})/(\d{2})/(\d{2})/$')
	def events_list(self, request, year=None, month=None, day=None, *args, **kwargs):
		self.additional_breadcrumbs = []
		self.year = year
		self.month = month
		self.day = day
		self.archive = True
		self.template = 'app/event_index_page.html'
		return Page.serve(self, request, *args, **kwargs)

	@route(r'^(\d{4})/(\d{2})/(\d{2})/(.+)/$')
	def event_detail(self, request, year, month, day, slug, *args, **kwargs):
		try:
			event = EventPage.objects.live().get(start_datetime__year=year, start_datetime__month=month, start_datetime__day=day, slug=slug)
		except EventPage.DoesNotExist:
			raise Http404

		if event.is_active():
			return redirect(event.get_url())

		event.additional_breadcrumbs = [({'title': event.title, 'url': event.get_url()})]
		return Page.serve(event, request, *args, **kwargs)

	@classmethod
	def can_create_at(cls, parent):
		# Only allow one instance
		return super().can_create_at(parent) and not cls.objects.exists()

	class Meta:
		verbose_name = 'Event Archive Index Page'
		verbose_name_plural = 'Event Archive Index Pages'


class EventPage(RoutablePageMixin, DefaultPage):
	EMAIL_SETTING_CHOICES = (
		('', '-- Use Default Global Setting --'),
		('enabled', 'Enabled'),
		('disabled', 'Disabled'),
	)
	event_type = models.ForeignKey('EventType', verbose_name='Event Type', null=True, on_delete=models.SET_NULL)
	summary = models.TextField(null=True, blank=True, default='', max_length=300, verbose_name='Summary')
	description = RichTextField(default='', verbose_name='Description')
	require_registration = models.BooleanField(default=False, verbose_name='Requires Registration')
	location_type = models.CharField(max_length=24, choices=EVENT_LOCATION_TYPE_CHOICES[1:], default='', verbose_name='Location Type', help_text="If online, no address is necessary")
	address_line_1 = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name='Address Line 1')
	address_line_2 = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name='Address Line 2')
	address_city = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name='City')
	address_state = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name='State')
	address_zipcode = models.CharField(max_length=255, default='', null=True, blank=True, verbose_name='Postal Code')
	start_datetime = models.DateTimeField(verbose_name='Date & Time', help_text="The date and time the event starts.")
	duration = models.DecimalField(decimal_places=2, max_digits=4, default=1, null=True, blank=True, help_text="In hours", verbose_name='Duration')
	cost = models.CharField(max_length=50, default='Free', help_text="If adding a price, please use the currency symbol, e.g. $, £, etc.")
	image = models.ForeignKey('wagtailimages.Image', verbose_name='Image', null=True, on_delete=models.SET_NULL, related_name='+', help_text='Recommended size: 350 W x 220 H')
	materials = RichTextField(blank=True, null=True, help_text='Content displayed when event is over')
	credentials = models.TextField(blank=True)

	email_setting = models.CharField(verbose_name='Send Registration Email', max_length=20, choices=EMAIL_SETTING_CHOICES, default='', blank=True, help_text='Select a setting for sending registration emails. This overrides the default global setting')
	email_recipients = models.CharField(verbose_name='Email Recipients', max_length=200, null=True, blank=True, help_text='Add registration email recipients separated by commas. This overrides the default global setting.')

	content_panels = Page.content_panels + [
		MultiFieldPanel([
			FieldPanel('email_setting'),
			FieldPanel('email_recipients', widget=AdminTagWidget),
		], heading="Email Settings", classname='collapsible collapsed'),
		MultiFieldPanel([
			FieldPanel('event_type'),
			FieldRowPanel([
				FieldPanel('require_registration'),
				FieldPanel('cost'),
			]),
			FieldPanel('start_datetime'),
			FieldPanel('duration'),
			FieldPanel('summary'),
			FieldPanel('description'),
			FieldPanel('credentials'),
			ImageChooserPanel('image'),
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
			FieldPanel('materials'),
		], heading="Materials"),
	]

	# Tabs
	edit_handler = TabbedInterface([
		ObjectList(content_panels, heading='Content'),
		AbstractBasePage.meta_panels,
	])

	parent_page_types = ['app.EventIndexPage']
	subpage_types = []

	search_fields = DefaultPage.search_fields + [
		index.SearchField('summary'),
		index.SearchField('description'),
	]

	class Meta:
		verbose_name = 'Event'
		verbose_name_plural = 'Events'
		ordering = ['start_datetime']

	@route(r'^$')
	def redirect_to_detail_view(self, request, *args, **kwargs):
		return redirect(self.get_url())

	@route(r'^calendar/$')
	def generate_ics(self, request, *args, **kwargs):
		def add_line_breaks_after_tags(item):
			return re.sub(r'(<\/(?:h1|h2|h3|h4|h5|h6|p)>|<br\/>)', r'\1\\r\\n', item)

		def reformat_cms_line_breaks(item):
			return item.replace('\r\n', '\\n').replace('\\r\\n\\r\\n', '\\r\\n')

		address_line_1 = self.address_line_1 if self.address_line_1 else ''
		address_line_2 = ' ' + self.address_line_2 if self.address_line_2 else ''
		city = ' ' + self.address_city + ',' if self.address_city else ''
		state = ' ' + self.address_state if self.address_state else ''
		zipcode = ' ' + self.address_zipcode if self.address_zipcode else ''
		location = 'Online' if self.location_type == 'online' else '{}{}{}{}{}'.format(address_line_1, address_line_2, city, state, zipcode)
		summary = self.title
		filename = 'Benefit_Mall_{}.ics'.format(self.title.replace(' ', '_'))
		settings_time_zone = pytz.timezone(settings.TIME_ZONE)
		start_datetime = self.start_datetime.astimezone(settings_time_zone)
		end_datetime = self.get_end_datetime().astimezone(settings_time_zone)
		now_datetime = datetime.datetime.now().astimezone(settings_time_zone)
		start = start_datetime.strftime('%Y%m%dT%H%M%S')
		end = end_datetime.strftime('%Y%m%dT%H%M%S')
		now = now_datetime.strftime('%Y%m%dT%H%M%S')
		description = 'Location Type: {}'.format(self.get_location_type_display())
		description += '\\n\\n{}'.format(html.unescape(strip_tags(add_line_breaks_after_tags(self.description))))
		description += '\\n{}'.format(html.unescape(self.credentials))

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
		content += 'DESCRIPTION:{}\n'.format(reformat_cms_line_breaks(description))
		content += 'LOCATION:{}\n'.format(reformat_cms_line_breaks(location))
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

	def clean(self):
		super().clean()
		errors = {}
		events = EventIndexPage.objects.first()
		if self.email_setting == 'enabled' and not (self.email_recipients or events.email_recipients_global):
			errors['email_recipients'] = ErrorList(['Email Recipients is required here or globally when Send Registration Emails is enabled'])
		if len(errors) > 0:
			raise ValidationError(errors)

	def __str__(self):
		return self.title

	def get_url(self):
		if self.is_active():
			base_page = self.get_parent()
		else:
			base_page = self.get_parent().specific.get_archive_page()
		return '{}{}{}/'.format(base_page.url, self.start_datetime.strftime('%Y/%m/%d/'), self.slug)

	def get_full_url(self, request=None):
		url_parts = self.get_url_parts(request=request)
		site_id, root_url, page_path = url_parts
		return root_url + self.get_url()

	def get_calendar_url(self, request=None):
		url_parts = self.get_url_parts(request=request)
		site_id, root_url, page_path = url_parts
		return root_url + page_path + 'calendar/'

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


@register_snippet
class EventType(models.Model):
	name = models.CharField(max_length=255, help_text='Type display name')
	slug = models.SlugField(unique=True, max_length=80, help_text='Lowercase alphanumberic version of the display name used in URLs')

	panels = [
		MultiFieldPanel([
			FieldPanel('name'),
			FieldPanel('slug'),
		], heading='Type'),
	]

	def __str__(self):
		return self.name

	class Meta:
		verbose_name = 'Event Type'
		verbose_name_plural = 'Event Types'
