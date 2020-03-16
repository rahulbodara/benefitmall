from django import forms
from wagtail.core.blocks import FieldBlock


class CustomChoiceBlock(FieldBlock):
    def __init__(self, choices=None, required=True, default=None, help_text=None, widget=None, **kwargs):
        self.field = forms.ChoiceField(choices=choices, required=required, help_text=help_text, widget=widget)
        super(CustomChoiceBlock, self).__init__(default=default, **kwargs)
