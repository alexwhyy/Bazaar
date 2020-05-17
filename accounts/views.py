from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User

from .forms import SignUpForm

# Create your views here.
def index(request):
	return render(request, 'accounts/index.html')

def profile(request, username):
	try:
		user_requested = User.objects.get(username=username)
	except:
		return render(request, 'requests/no_permissions.html')
	return render(request, 'accounts/profile.html', {'user_requested': user_requested})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/requests')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})