from .models.pages import DefaultPage
from .models.blog import BlogIndexPage, BlogPage

from modeltranslation.translator import TranslationOptions
from modeltranslation.decorators import register


@register(DefaultPage)
class DefaultPageTR(TranslationOptions):
    fields = (
        #'body',
    )


@register(BlogIndexPage)
class BlogIndexPageTR(TranslationOptions):
    fields = (
        #'body',
    )


@register(BlogPage)
class BlogPageTR(TranslationOptions):
    fields = (
        #'body',
    )
