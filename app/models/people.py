from django.db import models
from django.forms.widgets import CheckboxSelectMultiple
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface, FieldRowPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from app.models.pages import DefaultPage, AbstractBasePage
from wagtail.core.models import Page, Http404, TemplateResponse
from django.utils.text import slugify
from wagtail.images.models import Image
from wagtail.contrib.routable_page.models import RoutablePageMixin, route

from site_settings.views import get_page_meta_data

class BusinessType(models.Model):
	name = models.CharField(max_length=50)
	old_guid = models.CharField(max_length=40)

	panels = [
		MultiFieldPanel([
			FieldPanel('name'),
		], heading="Business Type"),
	]

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']


class State(models.Model):
	name = models.CharField(max_length=50)
	abbreviation = models.CharField(max_length=2)
	old_guid = models.CharField(max_length=40)

	panels = [
		MultiFieldPanel([
			FieldPanel('name'),
			FieldPanel('abbreviation'),
		], heading="State"),
	]

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']


class Division(models.Model):
	name = models.CharField(max_length=50)
	states = models.ManyToManyField(State, related_name='division_states')
	vice_president = models.ForeignKey('Person', related_name='division_vp', on_delete=models.PROTECT, null=True, blank=True)
	show_on_division_page = models.BooleanField(default=True)

	panels = [
		MultiFieldPanel([
			FieldPanel('name'),
			FieldPanel('vice_president'),
			FieldPanel('show_on_division_page'),
			FieldPanel('states', widget=CheckboxSelectMultiple),
		], heading="Division"),
	]

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']


class Location(models.Model):
	name = models.CharField(max_length=50)
	address_1 = models.CharField(max_length=50, null=True, blank=True)
	address_2 = models.CharField(max_length=50, null=True, blank=True)
	city = models.CharField(max_length=50, null=True, blank=True)
	state = models.ForeignKey(State, related_name='location_state', on_delete=models.PROTECT, null=True, blank=True)
	postal_code = models.CharField(max_length=50, null=True, blank=True)
	phone_number = models.CharField(max_length=50, null=True, blank=True)
	tollfree_number = models.CharField(max_length=50, null=True, blank=True)
	fax_number = models.CharField(max_length=50, null=True, blank=True)
	business_type = models.ManyToManyField(BusinessType, related_name='location_business_types')
	description = RichTextField(null=True, blank=True)
	latlng = models.CharField(max_length=255, null=True, blank=True)
	division = models.ForeignKey(Division, related_name='location_state', on_delete=models.PROTECT, null=True, blank=True)
	old_guid = models.CharField(max_length=40, null=True, blank=True)

	panels = [
		MultiFieldPanel([
			FieldPanel('name'),
			FieldPanel('business_type'),
			FieldPanel('division'),
			FieldPanel('description'),
		], heading="Division Info", classname="collapsible"),
		MultiFieldPanel([
			FieldPanel('address_1'),
			FieldPanel('address_2'),
			FieldPanel('city'),
			FieldPanel('state'),
			FieldPanel('postal_code'),
			FieldPanel('latlng'),
		], heading="Address", classname="collapsible collapsed"),
		MultiFieldPanel([
			FieldPanel('phone_number'),
			FieldPanel('tollfree_number'),
			FieldPanel('fax_number'),
		], heading="Phone Numbers", classname="collapsible collapsed"),
	]

	def lat(self):
		return self.latlng.split(',')[0]

	def lng(self):
		return self.latlng.split(',')[1]

	def get_url_slug(self):
		return slugify(self.name + ' ' + str(self.id))

	def __str__(self):
		return self.name

	class Meta:
		ordering = ['name']


class Person(models.Model):
	first_name = models.CharField(max_length=50)
	last_name = models.CharField(max_length=50)
	title = models.CharField(max_length=50)
	photo = models.ForeignKey(Image, blank=True, null=True, related_name="person_photo", on_delete=models.SET_NULL)
	location = models.ForeignKey(Location, related_name='person_location', on_delete=models.PROTECT)
	email = models.EmailField()
	show_email = models.BooleanField(default=False)
	is_executive = models.BooleanField(default=False)
	executive_order = models.IntegerField()
	bio = RichTextField(null=True, blank=True)
	is_archived = models.BooleanField(default=False)

	panels = [
		MultiFieldPanel([
			FieldPanel('first_name'),
			FieldPanel('last_name'),
			FieldPanel('title'),
			ImageChooserPanel('photo'),
			FieldPanel('location'),
			FieldPanel('email'),
			FieldPanel('show_email'),
			FieldPanel('is_archived'),
		], heading="Person Info", classname="collapsible"),
		MultiFieldPanel([
			FieldPanel('bio'),
		], heading="Bio", classname="collapsible"),
		MultiFieldPanel([
			FieldPanel('is_executive'),
			FieldPanel('executive_order'),
		], heading="Executive Info", classname="collapsible collapsed"),
	]

	def __str__(self):
		return '{} {}'.format(self.first_name, self.last_name)

	class Meta:
		ordering = ['last_name', 'first_name']


class LocationIndexPage(RoutablePageMixin, DefaultPage):
	subpage_types = []

	class Meta:
		verbose_name = 'Location Index Page'
		verbose_name_plural = 'Location Index Pages'

	@route(r'^$')
	def locaton_list(self, request, *args, **kwargs):
		context = super().get_context(request, **kwargs)
		self.additional_breadcrumbs = []

		locations = Location.objects.all().order_by('state__abbreviation', 'name')

		output = {}
		markers = []
		for loc in locations:
			if loc.state.abbreviation not in output:
				output[loc.state.abbreviation] = {'name': loc.state.name, 'locations': []}
			output[loc.state.abbreviation]['locations'].append(loc)
			markers.append({'name': loc.name, 'lat': loc.lat, 'lng': loc.lng})

		context['states'] = output
		context['markers'] = markers
		return TemplateResponse(request, self.get_template(request), context)

	@route(r'^(.+)/$')
	def news_page_detail(self, request, slug, *args, **kwargs):
		context = super().get_context(request, **kwargs)

		# Get news item
		try:
			slug_items = slug.split('-')
			location = Location.objects.get(id=slug_items[-1])

			self.additional_breadcrumbs = [({'title': location.name, 'url': self.get_url()+slug})]

			team = Person.objects.filter(location=location)
		except Location.DoesNotExist:
			raise Http404

		context['location'] = location
		context['team'] = team
		# context.update(get_page_meta_data(request, news_page))
		return TemplateResponse(request, "app/location_page.html", context)

	@classmethod
	def can_create_at(cls, parent):
		# Only allow one child instance
		return super(LocationIndexPage, cls).can_create_at(parent) and not cls.objects.exists()

	def get_full_url(self, request=None):
		url_parts = self.get_url_parts(request=request)
		site_id, root_url, page_path = url_parts
		return root_url + self.get_url()
