from copy import deepcopy
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
from datetime import datetime



class CarrierIndexPage(RoutablePageMixin, DefaultPage):
	subpage_types = []

	class Meta:
		verbose_name = 'Carrier Index Page'
		verbose_name_plural = 'Carrier Index Pages'

	@route(r'^$')
	def carrier_list(self, request, *args, **kwargs):
		context = super().get_context(request, **kwargs)
		self.additional_breadcrumbs = []

		states_filter = request.GET.get('states') or None
		insurance_filter = request.GET.get('type') or None

		carriers = cache.get('carriers')
		# Remove based on publish dates
		published_carriers = {}
		for id in carriers:
			carrier = carriers[id]
			# '2014-11-12T06:00:00.000Z'
			if (carrier['start_time'] == None or
					datetime.strptime(carrier['start_time'], '%Y-%m-%dT%H:%M:%S.%fZ') < datetime.now()
					) and (
					carrier['end_time'] == None or
					datetime.strptime(carrier['end_time'], '%Y-%m-%dT%H:%M:%S.%fZ') > datetime.now()):
				published_carriers[id] = carrier
			if 'Premier' in carrier['name']:
				check = carrier
		carriers = published_carriers

		out = {}
		by_insurance = {}
		by_state = {}
		filterable_states = set()
		filterable_insurance_types = set()

		if states_filter:
			states_filter = set(states_filter.split('|'))
			states_filter &= set(s.name for s in State.objects.all())  # Removes possible malicious states

			for id in carriers:
				carrier = deepcopy(carriers[id])  # We will modify this later, create a copy.
				if states_filter & set(carrier['available_states']):
					out[id] = carrier
		else:
			out = carriers

		# Out is filtered by states or it is just carriers
		# Either way, it contains all selectable insurance_types
		for id, carrier in out.items():
			filterable_insurance_types |= set(it['name'] for it in out[id]['available_insurance_types'])

		# If we were given an insurance filter that does not exist, throw it away
		if insurance_filter not in filterable_insurance_types:
			insurance_filter = ''

		if insurance_filter:
			new_list = {}
			for id in out:
				carrier = out[id]
				for it in carrier['available_insurance_types']:
					if it['name'] == insurance_filter:
						# Add this carrier's states to the filter selection since it has the selected insurance type
						filterable_states |= set(carrier['available_states'])
						new_list[id] = carrier
						break
			out = new_list
		else:
			for _, carrier in out.items():
				filterable_states |= set(carrier['available_states'])

		if states_filter:
			filterable_states -= states_filter

		searchable_states = list(filterable_states)
		searchable_states.sort()

		# Order carriers alphaetically
		carrier_order = []
		for id in out:
			carrier = out[id]
			carrier_order.append({'id': id, 'name': carrier['name']})
		carrier_order.sort(key=lambda x: x['name'].lower())
		for idx, val in enumerate(carrier_order):
			id = val['id']
			carrier = out[id]
			carrier['order'] = idx
		carrier_list = []
		for key, carrier in sorted(out.items(), key=lambda x: x[1]['order']):
			if states_filter:
				# Filter the available products by the ones available for this state
				carrier['available_products'] = list(filter(
					lambda available_product: any(
						available_product['name'] in insurance_type_entry['product_types']
						for chosen_state in states_filter
						for k, insurance_type_entry in carrier['available_states'].get(chosen_state, dict()).items()
						if k != 'name'  # Exclude name, since that is in the state datastructure too
					),

					carrier['available_products']
				))

				# Filter the available insurance types by the ones available for this state
				carrier['available_insurance_types'] = list(filter(
					lambda available_insurance_type: any(
						available_insurance_type['name'] in carrier['available_states'].get(chosen_state, set())
						for chosen_state in states_filter
					),

					carrier['available_insurance_types']
				))

			carrier_list.append(carrier)

		context['carriers'] = carrier_list
		context['type_filter'] = insurance_filter or ''
		context['states_filter'] = json.dumps(list(states_filter or []))
		context['states'] = State.objects.all()
		context['filterable_states'] = searchable_states
		context['filterable_insurance_types'] = json.dumps(list(filterable_insurance_types or []))

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
