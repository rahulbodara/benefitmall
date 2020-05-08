from django.db import models

from wagtail.core.models import Page
from wagtail.core.fields import StreamField, RichTextField
from wagtail.admin.edit_handlers import FieldPanel, StreamFieldPanel, MultiFieldPanel, TabbedInterface, ObjectList, InlinePanel, FieldRowPanel
from wagtail.contrib.forms.models import AbstractFormField, FORM_FIELD_CHOICES
from wagtail.contrib.forms.forms import FormBuilder
from wagtail.search import index

from modelcluster.fields import ParentalKey

from site_settings.models import AbstractBasePage, AbstractBaseEmailForm

from app.blocks import DefaultStreamBlock


class DefaultPage(AbstractBasePage):
    body = StreamField(DefaultStreamBlock(required=False), blank=True, null=True)
    body_below = StreamField(DefaultStreamBlock(required=False), blank=True, null=True)

    # Content Tab
    content_panels = Page.content_panels + [
        StreamFieldPanel('body'),
    ]

    # Unused but still causes an error if you remove it
    meta_panels = []

    # Tabs
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        AbstractBasePage.meta_panels,
    ])

    search_fields = AbstractBasePage.search_fields + [
        index.SearchField('body'),
        index.SearchField('body_below'),
    ]


class FormField(AbstractFormField):
    page = ParentalKey('FormPage', on_delete=models.CASCADE, related_name='form_fields')
    field_type = models.CharField(choices=FORM_FIELD_CHOICES, max_length=48)


class CustomFormBuilder(FormBuilder):
    pass


class FormPage(AbstractBaseEmailForm):

    text_above = StreamField(DefaultStreamBlock(required=False), blank=True, null=True)
    text_below = StreamField(DefaultStreamBlock(required=False), blank=True, null=True)
    thank_you_text = RichTextField(blank=True)

    # Content Tab
    content_panels = Page.content_panels + [
        StreamFieldPanel('text_above'),
        InlinePanel('form_fields', label="Form fields"),
        FieldPanel('thank_you_text', classname="full"),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Email"),
        StreamFieldPanel('text_below'),
    ]

    # Unused but still causes an error if you remove it
    meta_panels = []

    # Tabs
    edit_handler = TabbedInterface([
        ObjectList(content_panels, heading='Content'),
        AbstractBasePage.meta_panels,
    ])

    search_fields = AbstractBaseEmailForm.search_fields + [
        index.SearchField('text_above'),
        index.SearchField('text_below'),
    ]

    form_builder = CustomFormBuilder

    def get_form_fields(self):
        return self.form_fields.all()
