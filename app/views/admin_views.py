from django.views.generic.base import TemplateView
from app.models import Icon


class IconReference(TemplateView):
	template_name = 'wagtailadmin/icon_reference.html'

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['icons'] = Icon.objects.filter().order_by('category', 'title')
		return context