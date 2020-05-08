import datetime

from django import template
from django.template.loader import render_to_string
from django.utils.html import format_html
from django.shortcuts import redirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator

from wagtail.core.models import Site

from app.models import BlogPage, EventPage, NewsPage, Person, Division
from app.choices.block_edit_choices import BIO_LAYOUT_CHOICES, SUBHEAD_SIZE_CHOICES
from app.wagtail_hooks import HeaderFooter

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


@register.simple_tag(takes_context=True)
def render_person_list(context, layout=BIO_LAYOUT_CHOICES[0][0], title_size=SUBHEAD_SIZE_CHOICES[0][0], filter='all'):
    if filter == 'executives':
        people = Person.objects.filter(is_executive=True).order_by('executive_order')
    elif filter == 'sales':
        people = [div.vice_president for div in Division.objects.all().order_by('vice_president__last_name') if div.vice_president]
    else:
        people = Person.objects.all()

    person_list_context = {'people': people, 'layout': layout, 'title_size': title_size}
    return render_to_string('blocks/person_list_item_block.html', context=person_list_context, request=context['request'])


@register.simple_tag()
def get_recent_blogs(page, category, max_items):
    """
    Return recent blog posts, excluding current page.
    Optionally filter by category.
    """
    blogs = BlogPage.objects.live().exclude(id=page.id).order_by('-date')
    if category:
        blogs = blogs.filter(categories=category)
    return blogs[:int(max_items)]


@register.simple_tag()
def get_upcoming_events(page, event_type, location_type, max_items):
    """
    Return upcoming events, excluding current page.
    Optionally filter by event_type.
    """
    events = EventPage.objects.live().filter(start_datetime__date__gte=datetime.datetime.today()).exclude(id=page.id).order_by('start_datetime')
    if event_type:
        print('EVENT_TYPE:', event_type)
        events = events.filter(event_type=event_type)
    if location_type:
        print('LOCATION_TYPE:', location_type)
        events = events.filter(location_type=location_type)
    # Limit to active events only
    active_events = []
    for event in events:
        if event.is_active():
            active_events.append(event)
    return active_events[:int(max_items)]


@register.simple_tag()
def get_recent_news(page, max_items):
    """
    Return recent news items, excluding current page.
    """
    return NewsPage.objects.live().exclude(id=page.id).order_by('-news_datetime')[:int(max_items)]


@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    """
    Returns the URL-encoded querystring for the current page,
    updating the params with the key/value pairs passed to the tag.
    Also removes pipe-delimited params within _remove

    E.g: given the querystring ?foo=1&bar=2
    {% query_transform bar=3 %} outputs ?foo=1&bar=3
    {% query_transform foo='baz' %} outputs ?foo=baz&bar=2
    {% query_transform foo='one' _remove='bar|baz' %} outputs ?foo=one

    A RequestContext is required for access to the current querystring.
    """
    query = context['request'].GET.copy()
    remove = []
    for k, v in kwargs.items():
        if k == '_remove':
            remove = v.split('|')
        else:
            query[k] = v
    for k in remove:
        query.pop(k, None)
    return query.urlencode()


@register.simple_tag(takes_context=True)
def get_header_footer_field(context, field):
    """
    Returns value from supplied HeaderFooter field.
    """
    return getattr(HeaderFooter.for_site(site=get_current_site(context)), field)


@register.simple_tag(takes_context=True)
def get_events(context, page):
    """
    Returns events.
    """
    if page.archive is None:
        return None

    now = datetime.datetime.today()
    today = now.date()

    # Get requested date from URL
    url_date = datetime.datetime.strptime(
        '{year}-{month}-{day}'.format(
            year=page.year or today.year,
            month=page.month or today.month,
            day=page.day or today.day
        ),
        '%Y-%m-%d'
    ).date()

    events = EventPage.objects.live()

    # Archived events
    if page.archive:
        if url_date > today:
            return redirect(page.url)
        events = events.filter(start_datetime__lte=now).order_by('-start_datetime')
    # Upcoming events
    else:
        if url_date < today:
            return redirect(page.url)
        events = events.filter(start_datetime__gte=now).order_by('start_datetime')

    if page.year:
        events = events.filter(start_datetime__year=page.year)
    if page.month:
        events = events.filter(start_datetime__month=page.month)
    if page.day:
        events = events.filter(start_datetime__day=page.day)

    paginator = Paginator(events, 10)
    try:
        events = paginator.page(context['request'].GET.get('page'))  # Return linked page
    except PageNotAnInteger:
        events = paginator.page(1)  # Return first page
    except EmptyPage:
        events = paginator.page(paginator.num_pages)  # Return last page
    return events
