from django import template
from django.utils.html import format_html

from app.models import BlogPage


register = template.Library()


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
