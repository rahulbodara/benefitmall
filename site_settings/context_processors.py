from site_settings.wagtail_hooks import SiteSettings


def get_site_meta_data(request):
	meta_data = {
		'fav_icon': None,
		'apple_touch_icon': None,
		'pwa_use_manifest': False,
		'gtm_id': None,
	}
	try:
		site_settings = SiteSettings.for_site(site=request.site)

		if site_settings.favicon_ico:
			meta_data['fav_icon'] = site_settings.favicon_ico.file.url

		if site_settings.apple_touch_icon:
			meta_data['apple_touch_icon'] = site_settings.apple_touch_icon.file.url

		if site_settings.pwa_use_manifest:
			meta_data['pwa_use_manifest'] = True

		if site_settings.google_analytics_tag:
			meta_data['gtm_id'] = site_settings.google_analytics_tag
	except Exception as e:
		print('Error with get_site_meta_data:', e)

	return meta_data
