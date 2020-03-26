from django import forms
from django.apps import apps

class EventDetailWidget(forms.Widget):
	template_name = 'widgets/event_detail_widget.html'

	def get_context(self, name, value, attrs):
		context = super().get_context(name, value, attrs)
		EventPage = apps.get_model(app_label='app', model_name='EventPage')
		context['event'] = EventPage.objects.get(id=value)
		return context
