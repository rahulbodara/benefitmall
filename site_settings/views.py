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
        context['results_count'] = len(all_results)
        context['query'] = query
        return TemplateResponse(request, "search/search_results.html", context)
    else:
        raise Http404


def get_page_meta_data(request, page):
    # return the value you want as a dictionnary. you may add multiple values in there.
    meta_data = {
        'site_url': '',
        'site_name': '',
        'canonical_url': '',
        'meta_title': '',
        'meta_description': '',
        'meta_keywords': '',
        'og_title': '',
        'og_description': '',
        'og_type': '',
        'og_url': '',
        'og_image': '',
    }

    # Site URL
    site_url = request.site.root_page.get_full_url(request)
    meta_data['site_url'] = site_url

    # Site Name
    site_name = request.site.site_name
    meta_data['site_name'] = site_name

    # Current URL
    current_url = page.get_full_url(request)

    # Meta Title
    meta_title = page.seo_title or page.title
    meta_data['meta_title'] = meta_title + ' | ' + site_name

    # Meta Decription
    meta_description = page.search_description or ''
    meta_data['meta_description'] = meta_description

    # Meta Keywords
    meta_data['meta_keywords'] = page.meta_keywords or ''

    # Open Graph Title
    og_title = page.og_title or meta_title
    meta_data['og_title'] = og_title + ' | ' + site_name

    # Open Graph Description
    meta_data['og_description'] = page.og_description or meta_description

    # Open Graph Type
    meta_data['og_type'] = page.og_type or 'website'

    # Open Graph Image
    meta_data['og_image'] = page.og_image.file.url if page.og_image else ''

    # Open Graph URL
    meta_data['og_url'] = current_url

    # Canonical URL
    meta_data['canonical_url'] = page.canonical_url or current_url


    return meta_data
