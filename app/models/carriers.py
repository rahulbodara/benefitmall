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
from django.core.cache import cache
from app.models import State
import requests
import json



class CarrierIndexPage(RoutablePageMixin, DefaultPage):
	subpage_types = []

	class Meta:
		verbose_name = 'Carrier Index Page'
		verbose_name_plural = 'Carrier Index Pages'

	@route(r'^$')
	def carrier_list(self, request, *args, **kwargs):
		context = super().get_context(request, **kwargs)
		self.additional_breadcrumbs = []

		state_filter = request.GET.get('state') or None
		insurance_filter = request.GET.get('type') or None
		carriers = cache.get('carriers')
		out = {}
		by_insurance = {}
		by_state = {}
		if insurance_filter or state_filter:
			if insurance_filter:
				for id in carriers:
					carrier = carriers[id]
					for it in carrier['available_insurance_types']:
						if it['name'] == insurance_filter:
							by_insurance[id] = carrier
							break
			else:
				by_insurance = carriers
			if state_filter:
				for id in carriers:
					carrier = carriers[id]
					if state_filter in carrier['available_states']:
						by_state[id] = carrier
			else:
				by_state = carriers
			for id in by_insurance:
				if id in by_state:
					out[id] = by_insurance[id]
		else:
			out = carriers

		context['carriers'] = out
		context['type_filter'] = insurance_filter or ''
		context['state_filter'] = state_filter or ''
		context['states'] = State.objects.all()
		return TemplateResponse(request, self.get_template(request), context)

	@route(r'^(.+)/$')
	def carrier_page_detail(self, request, slug, *args, **kwargs):
		context = super().get_context(request, **kwargs)

		carrier_id = slug.split('-')[-1]

		carriers = cache.get('carriers')
		if carrier_id in carriers:
			carrier = carriers[carrier_id]
		else:
			raise Http404

		for i in range(len(carrier['products'])):
			for key, value in carrier['products'][i].items():
				if key not in ['small_group', 'large_group', 'self_funded', 'individual', 'senior', ]:
					continue
				states = carrier['products'][i][key]['states']
				carrier['products'][i][key]['states_list'] = json.dumps([state['name'] for state in states])

		context['carrier'] = carrier


		self.additional_breadcrumbs = [({'title': carrier['name'], 'url': self.get_url()+carrier['slug']})]
		# context.update(self.get_page_meta_data(request, location))
		return TemplateResponse(request, "app/carrier_page.html", context)

	@classmethod
	def can_create_at(cls, parent):
		# Only allow one child instance
		return super(CarrierIndexPage, cls).can_create_at(parent) and not cls.objects.exists()

	def get_carrier_url(self, carrier):
		return self.get_full_url() + slugify(carrier.name + ' ' + carrier.id)


	def get_full_url(self, request=None):
		url_parts = self.get_url_parts(request=request)
		site_id, root_url, page_path = url_parts
		return root_url + self.get_url()

	def get_page_meta_data(self, request, carrier):
		meta_data = { 'site_url': '', 'site_name': '', 'canonical_url': '', 'meta_title': '', 'meta_description': '', 'meta_keywords': '', 'og_title': '', 'og_description': '', 'og_type': '', 'og_url': '', 'og_image': '', }

		meta_data['site_url'] = request.site.root_page.get_full_url(request)
		site_name = request.site.site_name
		meta_data['site_name'] = site_name
		current_url = '{}{}'.format(self.get_full_url(request), carrier.get_url_slug())
		meta_title = '{} | Office Locations | {}'.format(carrier.name, site_name)
		meta_data['meta_title'] = meta_title
		meta_description = 'Carrier meta description'
		meta_data['meta_description'] = meta_description
		meta_data['og_title'] = meta_title
		meta_data['og_description'] = meta_description
		meta_data['og_type'] = 'website'
		meta_data['og_url'] = current_url
		meta_data['canonical_url'] = current_url

		return meta_data
