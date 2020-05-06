from django.conf import settings
from django.shortcuts import redirect
from django.http import HttpResponseNotFound, HttpResponseServerError
from wagtail.core.models import Site, Page
from app.models import DefaultPage
from django.template.loader import render_to_string
import uuid


class SecurityMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request.session['script_nonce'] = str(uuid.uuid4().hex)
        request.session['style_nonce'] = str(uuid.uuid4().hex)
        request.session['font_nonce'] = str(uuid.uuid4().hex)

        response = self.get_response(request)
        return response


class SiteSettingsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        try:
            use_csp = settings.USE_CSP_HEADER
        except Exception as ex:
            use_csp = False

        if use_csp and '/admin/' not in request.path:
            try:
                csp_exceptions = settings.USE_CSP_EXCEPTIONS
            except Exception as ex:
                csp_exceptions = []

            # Initialize CSP sections
            default_src = ["'none'"]
            base_uri = ["'self'"]
            form_action = ["'self'"]
            connect_src = ["'self'"]
            img_src = ["'self'"]
            script_src = ["'self'"]
            style_src = ["'self'"]
            font_src = ["'self'"]
            frame_src = ["'self'"]
            prefetch_src = ["'self'"]
            frame_ancestors = ["'none'"]
            response['Content-Security-Policy'] = ""

            # jquery, typekit, googlefonts, googlemaps, youtube, gtm, gtm_preview, gtm_custom_vars
            if 'salesforce' in csp_exceptions:
                # First include UA
                frame_src.append('https://*.salesforce.com')
                connect_src.append('https://*.salesforce.com')
                form_action.append('https://*.salesforce.com')
                script_src.append('https://*.salesforceliveagent.com')
                connect_src.append('https://*.salesforceliveagent.com')
                form_action.append('https://*.salesforceliveagent.com')


            if 'jquery' in csp_exceptions:
                connect_src.append('https://code.jquery.com')
                script_src.append("https://code.jquery.com")

            if 'typekit' in csp_exceptions:
                connect_src.append('https://*.typekit.net')
                font_src.append("https://*.typekit.net")
                style_src.append("https://*.typekit.net")

            if 'googlefonts' in csp_exceptions:
                connect_src.append('https://fonts.googleapis.com')
                connect_src.append('https://fonts.gstatic.com')
                style_src.append("https://fonts.googleapis.com")
                font_src.append("https://fonts.gstatic.com")

            if 'googlemaps' in csp_exceptions:
                frame_src.append("https://www.google.com")
                connect_src.append("https://www.google.com")
                script_src.append("https://*.googleapis.com")
                img_src.append("https://*.googleapis.com")
                script_src.append("https://*.gstatic.com")
                img_src.append("https://*.gstatic.com")
                connect_src.append("https://*.googleapis.com")
                connect_src.append("https://*.gstatic.com")
                img_src.append("data:")

            if 'youtube' in csp_exceptions:
                frame_src.append("https://www.youtube.com")
                connect_src.append("https://www.youtube.com")

            if 'vidyard' in csp_exceptions:
                script_src.append("https://*.vidyard.com")
                img_src.append("https://*.vidyard.com")
                connect_src.append("https://*.vidyard.com")
                frame_src.append("https://*.vidyard.com")
                prefetch_src.append("https://*.vidyard.com")
                # TODO - The browser doesn't support prefetch-src yet, so have to add to default-src for now.
                default_src.append("https://*.vidyard.com")

            if 'gtm' in csp_exceptions:
                # First include UA
                connect_src.append('https://www.google-analytics.com')
                script_src.append("https://www.google-analytics.com")
                script_src.append("https://ssl.google-analytics.com")
                img_src.append('https://www.google-analytics.com')
                # Then GTM
                frame_src.append('https://*.doubleclick.net')
                connect_src.append('https://*.doubleclick.net')
                connect_src.append('https://www.googletagmanager.com')
                script_src.append("'unsafe-inline'")
                script_src.append("https://www.googletagmanager.com")
                script_src.append("https://tagmanager.google.com")
                script_src.append("https://www.youtube.com")
                script_src.append("http://www.youtube.com")
                script_src.append("https://*.ytimg.com")
                script_src.append("https://www.googleadservices.com")
                script_src.append("https://www.google.com")
                script_src.append('https://*.doubleclick.net')
                style_src.append("https://tagmanager.google.com")
                style_src.append("https://fonts.googleapis.com")
                img_src.append('https://www.googletagmanager.com')
                img_src.append('https://www.gstatic.com')
                img_src.append('https://ssl.gstatic.com')
                img_src.append('https://*.doubleclick.net')
                img_src.append('https://www.google.com')
                font_src.append("https://fonts.gstatic.com")
                font_src.append("data:")
                # Then custom vars
                if 'gtm_custom_vars' in csp_exceptions:
                    script_src.append("'unsafe-eval'")
                if 'gtm_preview' in csp_exceptions:
                    script_src.append("https://tagmanager.google.com")
                    img_src.append('https://ssl.gstatic.com')
                    style_src.append("'unsafe-inline'")

            # Add media urls
            if settings.MEDIA_URL.startswith('http'):
                connect_src.append(settings.MEDIA_URL[0:-1])
                img_src.append(settings.MEDIA_URL[0:-1])

            if settings.STATIC_URL.startswith('http'):
                connect_src.append(settings.STATIC_URL[0:-1])
                img_src.append(settings.STATIC_URL[0:-1])

            if not "'unsafe-inline'" in script_src:
                script_src.append("'nonce-" + request.session['script_nonce'] + "'")
            if not "'unsafe-inline'" in style_src:
                style_src.append("'nonce-" + request.session['style_nonce'] + "'")
            if not "'unsafe-inline'" in font_src:
                font_src.append("'nonce-" + request.session['font_nonce'] + "'")


            # WRITE OUT CSP SETTINGS
            # BASE CSP SETTINGS
            response['Content-Security-Policy'] += "default-src " + ' '.join(default_src) + ";"
            response['Content-Security-Policy'] += " base-uri " + ' '.join(base_uri) + ";"
            response['Content-Security-Policy'] += " form-action " + ' '.join(form_action) + ";"
            response['Content-Security-Policy'] += " frame-ancestors " + ' '.join(frame_ancestors) + ";"
            response['Content-Security-Policy'] += " frame-src " + ' '.join(frame_src) + ";"
            response['Content-Security-Policy'] += " connect-src " + ' '.join(connect_src) + ";"
            response['Content-Security-Policy'] += " script-src " + ' '.join(script_src) + ";"
            response['Content-Security-Policy'] += " style-src " + ' '.join(style_src) + ";"
            response['Content-Security-Policy'] += " font-src " + ' '.join(font_src) + ";"
            response['Content-Security-Policy'] += " img-src " + ' '.join(img_src) + ";"
            response['Content-Security-Policy'] += " prefetch-src " + ' '.join(prefetch_src) + ";"

        response['Server'] = 'intentionally-undisclosed'
        response['Referrer-Policy'] = 'same-origin, strict-origin-when-cross-origin'

        return response


#  Redirect request to lowercased path if it contains uppercase letters
#  Redirect for 404 and 500
class CaseInsensitiveURLMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)

        if not request.path.startswith('/admin/'):

            #  Don't handle POST
            if request.method == 'GET':
                lowercase_path = request.path_info.lower()
                if request.path_info != lowercase_path:
                    return redirect(lowercase_path, permanent=True)

            if not settings.DEBUG:
                if response.status_code == 404 or response.status_code == 500:
                    header = 'Page Not Found' if response.status_code==404 else 'Server Error'
                    subheader = 'The page you requested was not found.' if response.status_code==404 else 'There was an error processing your request.'
                    if request and request.site:
                        root = request.site.root_page
                    else:
                        root = Site.objects.first().root_page
                    try:
                        error_page = Page.objects.child_of(root).filter(title=str(response.status_code)).first().specific
                    except Page.DoesNotExist as ex:
                        new_error_page = DefaultPage(title=str(response.status_code))
                        root.add_child(instance=new_error_page)
                        new_error_page.save()
                        error_page = new_error_page

                    content = render_to_string('app/default_page.html', context={'page': error_page}, request=request)

                    return HttpResponseNotFound(content) if response.status_code==404 else HttpResponseServerError(content)

        return response
