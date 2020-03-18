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
	event_title = models.CharField(max_length=255)
	event_type = models.CharField(max_length=24, choices=TYPE_CHOICES, default='')
	description = RichTextField(default='')

	location_type = models.CharField(max_length=24, choices=LOCATION_TYPE_CHOICES, default='', help_text="If online, no address is necessary")
	address_line_1 = models.CharField(max_length=255, default='', null=True, blank=True)
	address_line_2 = models.CharField(max_length=255, default='', null=True, blank=True)
	address_city = models.CharField(max_length=255, default='', null=True, blank=True)
	address_state = models.CharField(max_length=255, default='', null=True, blank=True)
	address_zipcode = models.CharField(max_length=255, default='', null=True, blank=True)

	start_datetime = models.DateTimeField()
	end_datetime = models.DateTimeField()

	cost = models.CharField(max_length=50, default='Free')


	panels = [
		MultiFieldPanel([
			FieldPanel('event_title'),
			FieldPanel('start_datetime'),
			FieldPanel('end_datetime'),
			FieldPanel('event_type'),
			FieldPanel('cost'),
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
