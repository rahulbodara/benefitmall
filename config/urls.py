from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
import requests

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls
from wagtail.contrib.sitemaps.views import sitemap
from site_settings import urls as site_settings_urls

from django.http import HttpResponse


def return_sw(request):
    f = requests.get(request.build_absolute_uri(settings.STATIC_URL+'sw.js'))
    return HttpResponse(f.text, content_type="text/javascript")


def return_favicon(request):
    f = requests.get(request.build_absolute_uri(settings.STATIC_URL+'favicon.ico'))
    return HttpResponse(f.content, content_type="image/x-icon")

def return_apple_touch_icon(request):
    f = requests.get(request.build_absolute_uri(settings.STATIC_URL+'icon.png'))
    return HttpResponse(f.content, content_type="image/png")

def return_tile(request):
    f = requests.get(request.build_absolute_uri(settings.STATIC_URL+'tile.png'))
    return HttpResponse(f.content, content_type="image/png")

def return_tile_wide(request):
    f = requests.get(request.build_absolute_uri(settings.STATIC_URL+'tile-wide.png'))
    return HttpResponse(f.content, content_type="image/png")



urlpatterns = [
    url(r'', include(site_settings_urls)),
    url('^sitemap\.xml$', sitemap),
    url(r'^django-admin/', admin.site.urls),
    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),
    url(r'', include(wagtail_urls)),
    url('^sw\.js$', return_sw),
    url('^favicon\.ico$', return_favicon),
    url('^icon\.png$', return_apple_touch_icon),
    url('^tile\.png$', return_tile),
    url('^tile_wide\.png$', return_tile_wide),
]

# urlpatterns += i18n_patterns(
#     # These URLs will have /<language_code>/ appended to the beginning
#     url(r'', include(wagtail_urls)),
# )

if settings.LOCAL_STATIC:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
