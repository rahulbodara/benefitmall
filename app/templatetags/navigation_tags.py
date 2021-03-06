from django import template
from django.template.loader import render_to_string
from app.wagtail_hooks import HeaderFooter
from site_settings.wagtail_hooks import SiteSettings
from wagtail.core.models import Site
from wagtail.core.models import Page
from app.models.notifications import Notification
from django.utils.html import escape
from wagtail.core.models import Page
from django.utils.safestring import mark_safe
from datetime import datetime
register = template.Library()
hard_exclude_in_sitemap = ['EventPage', 'BlogPage', 'NewsPage']
@register.simple_tag(takes_context=True)
def get_site_root(context):
    return context['request'].site.root_page


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


def has_children(page):
    return page.get_children().live().exists()


def is_active(page, current_page):
    return current_page.url.startswith(page.url) if current_page else False


def get_current_site(self, context=None):
    if context and context.request:
        site = context['request'].site
    else:
        site = Site.objects.first()
    return site


@register.simple_tag(takes_context=True)
def get_site_map(context):
    ret = mark_safe(get_page_items(get_site_root(context), context))
    return ret


def get_page_items(parent, context):
    ret = '<ul>'
    children = Page.objects.child_of(parent).live().specific()
    for page in children:
        if not page.hide_in_sitemap and page.specific.__class__.__name__ not in hard_exclude_in_sitemap:
            ret += '<li><a href="{1}">{0}</a>'.format(
                escape(page.title),
                get_path(page, context)
            )
            if has_children(page):
                ret += get_page_items(page, context)
            ret += '</li>'
    ret += '</ul>'
    return ret


def get_path(page, context):
    try:
        root_slug = context['request'].site.root_page.slug
        full_path = page.url_path
        rel_path = full_path[len(root_slug)+1:]
    except Exception as ex:
        tmp = ex
        rel_path = ''

    return rel_path


def get_links_recursive(context, parent, calling_page):
    menuitems = parent.get_children().live().in_menu().specific()
    for menuitem in menuitems:
        calling_page_url = calling_page.url
        menuitem_url = menuitem.url
        menuitem.active = (calling_page.url.startswith(menuitem.url) if calling_page.url else False)
        menuitem.destination = menuitem.url
        menuitem.show_dropdown = has_menu_children(menuitem)
        menuitem.destination = (get_path(menuitem, context) if menuitem.__class__.__name__ != 'NavigationItem' else menuitem.destination)
        if menuitem.show_dropdown:
            menuitem.children = get_links_recursive(context, menuitem, calling_page)
    return menuitems


def get_header_links(context, calling_page):
    site_root = get_current_site(context).root_page
    menuitems = get_links_recursive(context, site_root, calling_page)
    return menuitems

@register.simple_tag(takes_context=True)
def render_header(context, calling_page):
    if not calling_page:
        return ''
    if 'request' not in context:
        return ''

    header_footer = HeaderFooter.for_site(site=get_current_site(context))

    if header_footer.header_automatic_nav:
        header_links = get_header_links(context, calling_page)
    else:
        header_links = header_footer.header_links

    header_buttons = header_footer.header_buttons

    header_context = {
        'logo_url': header_footer.header_logo.file.url if header_footer.header_logo else None,
        'autonav': header_footer.header_automatic_nav,
        'header_links': header_links,
        'header_buttons': header_buttons,
        'header_utility_nav': header_footer.header_utility_nav,
        'utility_text': header_footer.utility_text,
        'utility_links': header_footer.utility_links,
        'header_banner_text_1': header_footer.header_banner_text_1,
        'header_banner_text_2': header_footer.header_banner_text_2,
        'copyright_text': header_footer.copyright_text,
        'social_facebook': header_footer.social_facebook,
        'social_instagram': header_footer.social_instagram,
        'social_twitter': header_footer.social_twitter,
        'social_linkedin': header_footer.social_linkedin,
        'social_youtube': header_footer.social_youtube,
    }

    return render_to_string('navigation/'+header_footer.navigation_type, context=header_context, request=context['request'])

@register.simple_tag(takes_context=True)
def render_footer(context):
    if 'request' not in context:
        return ''

    header_footer = HeaderFooter.for_site(site=get_current_site(context))

    footer_context = {
        'footer_links': header_footer.footer_links,
        'footer_category_links' : header_footer.footer_category_links,
        'footer_buttons': header_footer.footer_buttons,
        'footer_utility_links':header_footer.footer_utility_links,
        'tagline':header_footer.tagline,
        'logo_url': header_footer.footer_logo.file.url if header_footer.footer_logo else None,
        'copyright_text': header_footer.copyright_text,
        'social_facebook': header_footer.social_facebook,
        'social_instagram': header_footer.social_instagram,
        'social_twitter': header_footer.social_twitter,
        'social_linkedin': header_footer.social_linkedin,
        'social_youtube': header_footer.social_youtube,
    }

    return render_to_string('footer/'+header_footer.footer_type, context=footer_context, request=context['request'])


@register.simple_tag(takes_context=True)
def render_breadcrumbs(context, calling_page: Page):
    if not calling_page:
        return ''
    if 'request' not in context:
        return ''

    site = context['request'].site
    site_settings = SiteSettings.for_site(site=site)
    if not site_settings.show_breadcrumbs:
        return ''

    additional_breadcrumb_page_types = [
        'EventIndexPage',
        'NewsIndexPage',
        'LocationIndexPage',
        'PersonIndexPage',
        'CarrierIndexPage',
    ]

    menuitems = [m for m in calling_page.get_ancestors(True)][1:]
    if len(menuitems) <= 1:
        return ''
    if calling_page.specific.__class__.__name__ in additional_breadcrumb_page_types:
        menuitems.extend(calling_page.specific.additional_breadcrumbs)

    breadcrumb_context = {
        'menuitems': menuitems,
    }

    return render_to_string('navigation/breadcrumbs.html', context=breadcrumb_context, request=context['request'])

@register.simple_tag(takes_context=True)
def render_utility(context, calling_page):
    if not calling_page:
        return ''
    if 'request' not in context:
        return ''

    header_footer = HeaderFooter.for_site(site=get_current_site(context))

    utility_links = header_footer.utility_links

    utility_context = {
        'header_utility_nav': header_footer.header_utility_nav,
        'utility_background_color': header_footer.utility_background_color,
        'utility_switched': header_footer.utility_switched,
        'utility_text': header_footer.utility_text,
        'utility_links': utility_links,
    }

    return render_to_string('navigation/utility_nav.html', context=utility_context, request=context['request'])


@register.simple_tag(takes_context=True)
def render_notification(context, calling_page):
    if not calling_page:
        return ''
    if 'request' not in context:
        return ''



    if not Notification.objects.filter(starttime__lte=datetime.now(), endtime__gte=datetime.now()).exists():
        return ''
    else:
        notifications = Notification.objects.filter(starttime__lte=datetime.now(), endtime__gte=datetime.now()).first()

    notification_context = {
        'notification': notifications,
    }

    return render_to_string('navigation/notification.html', context=notification_context, request=context['request'])
