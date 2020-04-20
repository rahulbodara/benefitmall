from django import template
from django.template.loader import render_to_string
from django.utils.html import format_html
from wagtail.core.models import Site
from app.wagtail_hooks import HeaderFooter

from app.models import BlogPage
from app.models.events import EventPage
from app.models.people import Person, Division
from app.choices.block_edit_choices import BIO_LAYOUT_CHOICES, SUBHEAD_SIZE_CHOICES

register = template.Library()


def get_current_site(self, context=None):
    if context and context.request:
        site = context['request'].site
    else:
        site = Site.objects.first()
    return site


@register.simple_tag()
def format_paragraph(body, body_class):
    """
    Return body with outer <div> removed and conditionally added class to <p> tags.
    """
    if body and body_class:
            body = str(body)
            body = body.replace('<div class="rich-text">', '')
            body = body.replace('</div>', '')
            body = body.replace('<p>', '<p class="{}">'.format(body_class))
            return format_html(body)
    return body


@register.simple_tag()
def format_hr(alignment):
    """
    Return an <hr> tag with conditionally added styles.
    """
    if alignment == 'text-center':
        style = 'style=margin-left:auto;margin-right:auto;'
    elif alignment == 'text-right':
        style = 'style=margin-left:auto;'
    else:
        style = ''
    return format_html('<hr class="short" {}>'.format(style))


@register.simple_tag()
def format_blog_content(content):
    """
    Return body with outer <div> removed and conditionally added class to <p> tags.
    """
    if content:
            content = str(content)
            content = content.replace('<ul>', '<ul class="bullets">')
            return format_html(content)
    return content


@register.simple_tag()
def get_recent_posts(current_page):
    """
    Return 3 most recent blog posts, excluding current page.
    """
    return BlogPage.objects.live().exclude(id=current_page.id).order_by('-date')[:3]

@register.simple_tag(takes_context=True)
def render_person_list(context, layout=BIO_LAYOUT_CHOICES[0][0], title_size=SUBHEAD_SIZE_CHOICES[0][0], filter='all'):
    if filter == 'executives':
        people = Person.objects.filter(is_executive=True).order_by('executive_order')
    elif filter == 'sales':
        people = [div.vice_president for div in Division.objects.all() if div.vice_president]
    else:
        people = Person.objects.all()

    person_list_context = {'people': people, 'layout': layout, 'title_size': title_size}
    return render_to_string('blocks/person_list_item_block.html', context=person_list_context, request=context['request'])
