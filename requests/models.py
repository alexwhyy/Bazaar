from django.db import models
from datetime import datetime
from django.contrib.auth.models import User

# Create your models here.
class OrderRequest(models.Model):
	title = models.CharField(null=True, blank=False, max_length=255, help_text='Describe this order in a few short words.')
	address = models.CharField(null=True, blank=True, max_length=255, help_text='Address of where this request should be delivered.')
	order_body = models.TextField('Order', null=True, blank=False, help_text='Enter your order here.')

	creation_timestamp = models.DateTimeField(default=datetime.now)
	request_to = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_to')
	request_from = models.ForeignKey(User, on_delete=models.CASCADE, related_name='request_from')

	'''
	PENDING -> REJECTED
	PENDING -> WITHDRAWN
	PENDING -> ACCEPTED -> DONE
	'''
	status = models.CharField(default='PENDING', null=True, blank=True, max_length=255)

	def __str__(self):
		return self.title