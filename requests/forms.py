from django.db import models
from django.contrib.auth.models import User

from django import forms
from .models import OrderRequest

class OrderForm(forms.ModelForm):
	to_username = forms.CharField(label='Recipient', max_length=255, help_text='Bazaar recipient username.')

	# Adding the option to pass in the current user inside the form
	def __init__(self, *args, **kwargs):
		self.from_username = kwargs.pop('from_username', None)
		super(OrderForm, self).__init__(*args, **kwargs)

	class Meta:
		model = OrderRequest
		fields = ['title', 'address', 'order_body']

	def clean_to_username(self):
		username = self.cleaned_data['to_username']
		try:
			user = User.objects.exclude(pk=self.instance.pk).get(username=username)
		except User.DoesNotExist:
			raise forms.ValidationError('The username specified does not exist.')
		if username == self.from_username:
			raise forms.ValidationError('You cannot send a request to yourself! Nice try through.')
		return username

	def save(self):
		new_order = OrderRequest(title=self.cleaned_data['title'], address=self.cleaned_data['address'], order_body=self.cleaned_data['order_body'], request_to=User.objects.get(username=self.cleaned_data['to_username']), request_from=User.objects.get(username=self.from_username))
		new_order.save()