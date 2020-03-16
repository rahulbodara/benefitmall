from django import template
from django.template.loader import render_to_string
from app.wagtail_hooks import HeaderFooter
from wagtail.core.models import Site
register = template.Library()


@register.simple_tag(takes_context=True)
def get_site_root(context):
    return context['request'].site.root_page


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


def is_active(page, current_page):
    return current_page.url.startswith(page.url) if current_page else False


def get_current_site(self, context=None):
    if context and context.request:
        site = context['request'].site
    else:
        site = Site.objects.first()
    return site


def get_links_recursive(context, parent, calling_page):
    menuitems = parent.get_children().live().in_menu().specific()
    for menuitem in menuitems:
        menuitem.active = (calling_page.url.startswith(menuitem.url) if calling_page.url else False)
        menuitem.destination = menuitem.url
        menuitem.show_dropdown = has_menu_children(menuitem)
        if menuitem.show_dropdown:
            menuitem.children = get_links_recursive(context, menuitem, calling_page)
    return menuitems


def get_header_links(context, calling_page):
    site_root = get_current_site(context).root_page
    menuitems = get_links_recursive(context, site_root, calling_page)
    return menuitems


@register.simple_tag(takes_context=True)
def render_header(context, calling_page):
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
    header_footer = HeaderFooter.for_site(site=context.request.site)

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




