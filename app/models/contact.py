from django.db import models
from django import forms
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.template.loader import render_to_string

from wagtail.core.fields import RichTextField
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel, ObjectList, StreamFieldPanel, TabbedInterface
from wagtail.core.models import Page, Http404
from wagtail.admin.widgets import AdminTagWidget

from app.models import DefaultPage, AbstractBasePage, State


class ContactPage(DefaultPage):
	topics = models.CharField(max_length=1000, help_text='List of form topics. Separated by commas.')
	email_recipients = models.CharField(verbose_name='Recipients', max_length=1000, help_text='List of email addresses in order of respective topic. Separated by commas.')
	email_from = models.EmailField(verbose_name='From')
	email_subject = models.CharField(verbose_name='Subject', max_length=200)
	email_subject_user = models.CharField(verbose_name='Subject', max_length=200)
	instruction_message = RichTextField(verbose_name='Instruction Message', blank=True, null=True, help_text='Message that appears above form before submission.')
	confirmation_message = RichTextField(verbose_name='Confirmation Message', help_text='Message that appears in place of form after submission.')

	# Content Tab
	content_panels = Page.content_panels + [
		StreamFieldPanel('body'),
		FieldPanel('instruction_message', classname='full'),
		FieldPanel('confirmation_message', classname='full'),
		FieldPanel('topics', widget=AdminTagWidget),
		MultiFieldPanel([
			FieldPanel('email_from'),
		], heading='Email'),
		MultiFieldPanel([
			FieldPanel('email_subject'),
			FieldPanel('email_recipients'),
		], heading='Email to BenefitMall'),
		MultiFieldPanel([
			FieldPanel('email_subject_user'),
		], heading='Email to User'),
		StreamFieldPanel('body_below'),
	]

	# Tabs
	edit_handler = TabbedInterface([
		ObjectList(content_panels, heading='Content'),
		AbstractBasePage.meta_panels,
	])

	@classmethod
	def can_create_at(cls, parent):
		# Only allow one instance
		return super().can_create_at(parent) and not cls.objects.exists()

	def serve(self, request):
		sent = request.GET.get('sent', None)
		topics_list = self.topics.replace('"', '').split(',')
		topic_choices = [(topic, topic) for topic in topics_list]
		state_choices = [('{} - {}'.format(state.name, state.abbreviation), '{} - {}'.format(state.name, state.abbreviation)) for state in State.objects.all()]

		if request.method == 'POST' and not sent:
			form = ContactForm(request.POST, topic_choices=topic_choices, state_choices=state_choices)
			if form.is_valid():

				topic = form.cleaned_data['topic']
				email = form.cleaned_data['email']
				context = {
					'topic': topic,
					'first_name': form.cleaned_data['first_name'],
					'last_name': form.cleaned_data['last_name'],
					'email': email,
					'state': form.cleaned_data['state'],
					'phone': form.cleaned_data['phone'],
				}

				topic_index = topics_list.index(topic)
				recipient = self.email_recipients.split(',')[topic_index]
				recipient_list = recipient.split('/')
				print('RECIPIENTS:', topic_index, self.email_recipients.split(','))
				# Email to BenefitMall
				message = render_to_string('emails/contact_form_message.txt', context)
				message_html = render_to_string('emails/contact_form_message.html', context)
				send_mail(
					subject=self.email_subject,
					from_email=self.email_from,
					recipient_list=recipient_list,
					message=message,
					html_message=message_html
				)

				# Email to User
				message = render_to_string('emails/contact_form_message_user.txt', context)
				message_html = render_to_string('emails/contact_form_message_user.html', context)
				send_mail(
					subject=self.email_subject_user,
					from_email=self.email_from,
					recipient_list=[email],
					message=message,
					html_message=message_html
				)
				return redirect(self.url+'?sent=yes')
		else:
			form = ContactForm(topic_choices=topic_choices, state_choices=state_choices)

		self.form = form
		self.sent = sent
		return super().serve(request)


class ContactForm(forms.Form):
	def __init__(self, *args, **kwargs):
		topic_choices = kwargs.pop('topic_choices')
		state_choices = kwargs.pop('state_choices')
		super().__init__(*args, **kwargs)
		self.fields['topic'].choices = topic_choices
		self.fields['state'].choices = state_choices

	topic = forms.ChoiceField(widget=forms.RadioSelect)
	first_name = forms.CharField(max_length=200, label='First Name')
	last_name = forms.CharField(max_length=200, label='Last Name')
	email = forms.EmailField(max_length=200)
	state = forms.ChoiceField()
	phone = forms.CharField(max_length=200, required=False)
