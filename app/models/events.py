from django.db import models
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface, FieldRowPanel


class Event(models.Model):
	LOCATION_TYPE_CHOICES = (
		('online', 'Online'),
		('in_person', 'In Person'),
	)
	TYPE_CHOICES = (
		('benefits_meeting', 'Benefits Meeting'),
		('benefits_training', 'Benefits Training'),
		('webcast', 'Compliance Webcast'),
		('tradeshow', 'Tradeshow'),
	)
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
		], heading="Event",),
		MultiFieldPanel([
			FieldPanel('location_type'),
			FieldPanel('address_line_1'),
			FieldPanel('address_line_2'),
			FieldPanel('address_city'),
			FieldPanel('address_state'),
			FieldPanel('address_zipcode'),
		], heading="Location", ),

	]

	def __str__(self):
		return self.event_title

	class Meta:
		ordering = ['start_datetime']
