from django.template.loader import render_to_string

from wagtail.core.blocks import StructBlock, TextBlock


class DividerBlock(StructBlock):
    def __init__(self, icon=None, heading=None, **kwargs):
        self.icon = icon
        self.heading = heading
        super().__init__(**kwargs)

    def render_form(self, value, prefix='', errors=None):
      context = self.get_form_context(value, prefix=prefix, errors=errors)
      context['icon'] = self.icon
      context['heading'] = self.heading
      return render_to_string('blocks/divider_block.html', context)
