import os
from django.conf import settings
import requests
from django.utils.html import format_html, mark_safe
from django import template
register = template.Library()


@register.simple_tag(takes_context=True)
def allow_script(context):
	try:
		request = context.request
	except Exception as ex:
		request = context.dicts[1]['request']
	nonce = request.session['script_nonce']
	output = format_html('nonce="' + nonce + '"')
	return output


@register.simple_tag(takes_context=True)
def allow_font(context):
	try:
		request = context.request
	except Exception as ex:
		request = context.dicts[1]['request']
	nonce = request.session['font_nonce']
	output = format_html('nonce="' + nonce + '"')
	return output


@register.simple_tag(takes_context=True)
def allow_style(context):
	try:
		request = context.request
	except Exception as ex:
		request = context.dicts[1]['request']
	nonce = request.session['style_nonce']
	output = format_html('nonce="' + nonce + '"')
	return output

@register.simple_tag
def get_setting(name):
	return getattr(settings, name, "")
