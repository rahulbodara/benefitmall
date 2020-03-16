import os
from django.conf import settings
import requests
from django.utils.html import format_html, mark_safe
from wagtail.core.models import Site
from django import template
register = template.Library()
from wagtail.core.models import Page


@register.simple_tag
def get_setting(name):
	return getattr(settings, name, "")


