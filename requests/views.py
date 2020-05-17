from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, HttpResponseNotAllowed
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test

from .models import OrderRequest
from .forms import OrderForm

import os

# Create your views here.
@login_required
def index(request):
	context = {'GOOGLE_MAPS_STATIC_KEY': os.environ['GOOGLE_MAPS_STATIC_KEY'], 'incoming_requests': OrderRequest.objects.filter(request_to=request.user).order_by('-creation_timestamp'), 'outgoing_requests': OrderRequest.objects.filter(request_from=request.user).order_by('-creation_timestamp')}
	return render(request, 'requests/index.html', context=context)

@login_required
def detail(request, pk):
	try:
		order = OrderRequest.objects.get(pk=pk)
	except:
		# If it doesn't exist just give them the no permissions page
		return render(request, 'requests/no_permissions.html')
	context = {'order_request': order, 'GOOGLE_MAPS_STATIC_KEY': os.environ['GOOGLE_MAPS_STATIC_KEY']}
	if request.user == order.request_to:
		return render(request, 'requests/detail_incoming.html', context=context)
	elif request.user == order.request_from:
		return render(request, 'requests/detail_outgoing.html', context=context)
	else:
		return render(request, 'requests/no_permissions.html')

@login_required
def item_action(request, pk, action):
	try:
		order = OrderRequest.objects.get(pk=pk)
	except:
		return render(request, 'requests/no_permissions.html')
	
	# This is a really, really terrible idea but this is a hackathon so whatever.
	if action == 'accept' and order.status == 'PENDING':
		order.status = 'ACCEPTED'
		order.save()
	elif action == 'reject' and order.status == 'PENDING':
		order.status = 'REJECTED'
		order.save()
	elif action == 'withdraw' and order.status == 'PENDING':
		order.status = 'WITHDRAWN'
		order.save()
	elif action == 'done' and order.status == 'ACCEPTED':
		order.status = 'DONE'
		order.save()
	else:
		# I'm really too lazy to deal with error codes right now.
		return HttpResponse('<h1>Unable to Process Request</h1>')
	return redirect('index')

@login_required
def create(request):
	if request.method == 'GET':
		context = {'form': OrderForm}
	elif request.method == 'POST':
		form = OrderForm(request.POST, from_username=request.user)
		if form.is_valid():
			form.save()
			return redirect('index')
		else:
			# This is the same form object in which we have identified the errors for
			context = {'form': form}
	return render(request, 'requests/create.html', context=context)