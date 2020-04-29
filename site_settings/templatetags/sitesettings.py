import os
from django.conf import settings
import requests
from django.utils.html import format_html, mark_safe
from django.template.loader import render_to_string
from wagtail.core.models import Site
from django import template
register = template.Library()
from wagtail.core.models import Page
from site_settings.wagtail_hooks import SiteSettings


@register.simple_tag
def get_setting(name):
	return getattr(settings, name, "")


@register.simple_tag(takes_context=True)
def render_search_button(context):
	return render_search_item(context, 'button')


@register.simple_tag(takes_context=True)
def render_search_modal(context):
	return render_search_item(context, 'modal')


@register.simple_tag()
def render_search_item(context, item):
	try:
		if context and 'request' in context:
			site = context['request'].site
		else:
			site = Site.objects.first()
		site_settings = SiteSettings.for_site(site=site)
	except Exception as ex:
		e = ex
		site_settings = None
	if item == 'modal':
		template = 'search/search_modal.html'
	if item == 'button':
		template = 'search/search_button.html'
	return render_to_string(template) if site_settings.show_search else ''


@register.simple_tag()
def get_page_type(page):
	class_name = page.specific.__class__.__name__
	if class_name == 'EventPage':
		return 'Event'
	else:
		return ''
