from site_settings import views
from django.conf.urls import url
from site_settings.wagtail_hooks import SiteSettings

urlpatterns = [
    url(r'^search/$', views.search, name='search'),
    url(r'^robots.txt$', views.robots_txt, name='robots_txt'),
    url(r'^pwa_manifest.json$', views.pwa_manifest, name='pwa_manifest'),

]
