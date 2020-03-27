from django.http import HttpResponseRedirect, HttpResponseNotFound, HttpResponse, JsonResponse, Http404
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from wagtail.core.models import Page, TemplateResponse
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


def search(request):
    site_settings = SiteSettings.for_site(site=request.site)
    if site_settings.show_search:
        context = {}
        query = request.GET.get('q', None)
        results = []

        if query:
            all_results = Page.objects.live().search(query)

            paginator = Paginator(all_results, 10)

            try:
                # Return linked page
                results = paginator.page(request.GET.get('page'))
            except PageNotAnInteger:
                # Return first page
                results = paginator.page(1)
            except EmptyPage:
                # Return last page
                results = paginator.page(paginator.num_pages)

        context['page'] = Page.objects.get(slug='home')
        context['results'] = results
        context['results_count'] = len(results)
        context['query'] = query
        return TemplateResponse(request, "search/search_results.html", context)
    else:
        raise Http404
