from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, JsonResponse, Http404
from site_settings.wagtail_hooks import SiteSettings
import json

import logging
logger = logging.getLogger(__name__)
del logging  # To prevent accidentally using it


def robots_txt(request):
    robots = SiteSettings.for_site(site=request.site).robots_txt
    return HttpResponse(robots, content_type='text/plain')


def pwa_manifest(request):
    site_settings = SiteSettings.for_site(site=request.site)
    output = {}
    if site_settings.pwa_use_manifest:

        output = {
            'short_name': site_settings.pwa_short_name,
            'name': site_settings.pwa_name,
            'icons': [],
            'start_url': site_settings.pwa_start_url,
            'background_color': site_settings.pwa_background_color,
            'orientation': site_settings.pwa_orientation,
            'display': site_settings.pwa_display,
            'scope': site_settings.pwa_scope,
            'theme_color': site_settings.pwa_theme_color,
        }

        if site_settings.pwa_icon_small:
            output['icons'].append({
                'src': site_settings.pwa_icon_small.file.url,
                'type': "image/png",
                'sizes': "192x192"
            })
        if site_settings.pwa_icon_large:
            output['icons'].append({
                "src": site_settings.pwa_icon_large.file.url,
                "type": "image/png",
                "sizes": "512x512"
            })

        return HttpResponse(json.dumps(output), content_type='text/json')
    else:
        # Manifest is turned off, return a 404
        raise Http404
        # return HttpResponseNotFound()

