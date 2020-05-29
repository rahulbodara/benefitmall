from django.db import models
from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, InlinePanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface, FieldRowPanel

NOTIFICATION_WIDTH_CHOICES = (
    ('col-md-3', 'Extra Small'),
    ('col-md-4', 'Small'),
    ('col-md-6', 'Med'),
    ('col-md-12', 'Large'),
)

NOTIFICATION_LOCATION_CHOICES = (
    ('pos-top pos-left', 'Top Left'),
    ('pos-top pos-right', 'Top Right'),
    ('pos-bottom pos-left', 'Bottom Left'),
    ('pos-bottom pos-right', 'Bottom Right'),
)

BACKGROUND_MODE_CHOICES_NO_IMAGE = (
    ('bg--white', 'Light'),
    ('bg--primary', 'Primary'),
    ('bg--secondary', 'Secondary'),
    ('bg--dark', 'Dark'),
)

HORIZONTAL_ALIGNMENT_CHOICES = (
    (' ', 'Align Left'),
    ('text-center', 'Align Center'),
    ('text-right', 'Align Right'),
)
class Notification(models.Model):
    size = models.CharField(max_length=50, choices=NOTIFICATION_WIDTH_CHOICES, default=NOTIFICATION_WIDTH_CHOICES[0][0])
    location = models.CharField(max_length=50, choices=NOTIFICATION_LOCATION_CHOICES, default=NOTIFICATION_LOCATION_CHOICES[0][0])
    starttime = models.DateTimeField(verbose_name='Published Date', help_text="The date and time of the start of notification.")
    endtime = models.DateTimeField(verbose_name='Unpublished Date', help_text="The date and time of the end of notification.")
    text_alignment = models.CharField(max_length=50, choices=HORIZONTAL_ALIGNMENT_CHOICES, default=HORIZONTAL_ALIGNMENT_CHOICES[0][0], null=True, blank=True)
    header = models.CharField(max_length=255, verbose_name='Title')
    body = RichTextField(default='', verbose_name='Body', features=['bold', 'italic', 'ol', 'ul', 'hr', 'link', 'document-link'])
    background_color = models.CharField(max_length=50, choices=BACKGROUND_MODE_CHOICES_NO_IMAGE, default=BACKGROUND_MODE_CHOICES_NO_IMAGE[0][0])


    panels = [
        MultiFieldPanel([
            # FieldPanel('size'),
            # FieldPanel('location'),
            FieldPanel('starttime'),
            FieldPanel('endtime'),
            FieldPanel('text_alignment'),
            FieldPanel('header'),
            FieldPanel('body'),
            FieldPanel('background_color'),
        ], heading="Notifications"),
    ]



    def __str__(self):
        return self.header

    class Meta:
        ordering = ['starttime']

