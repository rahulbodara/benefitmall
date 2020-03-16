from wagtail.core.models import Page
from site_settings.wagtail_hooks import SiteSettings
from django.utils.html import format_html


def site_settings(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    output = {
        'PWA_MANIFEST': '',
        'GTM_HEADER': '',
        'GTM_BODY': '',
        'FAVICON': '',
        'APPLE_TOUCH_ICON': '',
    }

    try:
        settings_for_site = SiteSettings.for_site(site=request.site)

        if settings_for_site.favicon_ico:
            output['FAVICON'] = format_html('<link rel="icon" href="' + settings_for_site.favicon_ico.file.url + '">')

        if settings_for_site.favicon_ico:
            output['APPLE_TOUCH_ICON'] = format_html('<link rel="apple-touch-icon" href="' + settings_for_site.apple_touch_icon.file.url + '">')

        if settings_for_site.pwa_use_manifest:
            output['PWA_MANIFEST'] = format_html("<link rel=\"manifest\" href=\"/pwa_manifest.json\">")

        if settings_for_site.google_analytics_tag:
            output['GTM_HEADER'] = format_html("\
                <!-- Google Tag Manager -->\
                <script>(function(w,d,s,l,i){w[l]=w[l]||[];w[l].push({'gtm.start':\
                new Date().getTime(),event:'gtm.js'});var f=d.getElementsByTagName(s)[0],\
                j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=\
                'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);\
                })(window,document,'script','dataLayer','" + settings_for_site.google_analytics_tag + "');</script>\
                <!-- End Google Tag Manager -->")

            output['GTM_BODY'] = format_html("\
                <!-- Google Tag Manager (noscript) -->\
                <noscript><iframe src=\"https://www.googletagmanager.com/ns.html?id=" + settings_for_site.google_analytics_tag + "\"\
                height=\"0\" width=\"0\" style=\"display:none;visibility:hidden\"></iframe></noscript>\
                <!-- End Google Tag Manager (noscript) -->")

    except Exception:
        output = {}  # Clear it, we were unable to get the Site object or something else required
    return output


def meta_data(request):
    # return the value you want as a dictionnary. you may add multiple values in there.
    ret = {
        'PAGE_METADATA': '',
        'canonical_url': '',
        'meta_title': '',
        'meta_description': '',
        'meta_keywords': '',
        'og_title': '',
        'og_type': '',
        'og_url': '',
        'og_image': '',
        'og_description': '',
        'site_name': '',
        'site_url': '',
        'current_url': '',
    }
    try:
        site = request.site
        root = site.root_page
        site_root_url = root.get_full_url(request)
        ret['site_url'] = site_root_url
        site_name = site.site_name
        ret['site_name'] = site_name
        page_path = '/' + request.site.root_page.slug + request.path

        try:
            page = Page.objects.get(url_path=page_path).specific
        except Exception:
            page = Page.objects.child_of(root).get(title='404').specific

        if page:
            current_url = page.get_full_url(request)
            canonical_url = page.canonical_url if page.canonical_url else page.get_full_url(request)
            meta_title = page.seo_title + ' | ' + site_name if page.seo_title else page.title + ' | ' + site_name
            meta_description = page.search_description
            meta_keywords = page.meta_keywords
            og_title = page.og_title + ' | ' + site_name if page.og_title else page.seo_title + ' | ' + site_name if page.seo_title else page.title + ' | ' + site_name
            og_type = page.og_type if page.og_type else "website"
            og_url = current_url
            og_image = page.og_image.file.url if page.og_image else None
            og_description = page.og_description if page.og_description else page.search_description

            if current_url:
                ret['meta_title'] = meta_title
            if current_url:
                ret['current_url'] = current_url
            if canonical_url:
                ret['canonical_url'] = canonical_url
                ret['PAGE_METADATA'] += '<link rel="canonical" href="' + canonical_url + '" />'
            if meta_description:
                ret['meta_description'] = meta_description
                ret['PAGE_METADATA'] += '<meta name="description" content="' + meta_description + '" />'
            if meta_keywords:
                ret['meta_keywords'] = meta_description
                ret['PAGE_METADATA'] += '<meta name="keywords" content="' + meta_keywords + '" />'
            if og_description:
                ret['og_description'] = og_description
                ret['PAGE_METADATA'] += '<meta property="og:description" content="' + og_description + '" />'
                ret['PAGE_METADATA'] += '<meta name="twitter:card" value="' + og_description + '" />'
            if og_title:
                ret['og_title'] = og_title
                ret['PAGE_METADATA'] += '<meta property="og:title" content="' + og_title + '" />'
            if og_type:
                ret['og_type'] = og_type
                ret['PAGE_METADATA'] += '<meta property="og:type" content="' + og_type + '" />'
            if og_url:
                ret['og_url'] = og_url
                ret['PAGE_METADATA'] += '<meta property="og:url" content="' + og_url + '" />'
            if og_image:
                ret['og_image'] = og_image
                ret['PAGE_METADATA'] += '<meta property="og:image" content="' + og_image + '" />'
            ret['PAGE_METADATA'] = format_html(ret['PAGE_METADATA'])
    except Exception:
        ret = {}  # Clear it, we were unable to get the Site object or something else required

    return ret

