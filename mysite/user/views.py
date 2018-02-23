#from django.contrib.auth import forms as auth_forms, views as auth_views
from django.contrib.auth import login as auth_login, authenticate as auth_authenticate
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from user.forms import SignUpForm


def login(request):
	return render(request, 'user/login.html')

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = auth_authenticate(username=username, password=raw_password)
            auth_login(request, user)
            return redirect('/home')
    else:
        form = SignUpForm()

    return render(request, 'user/signup.html', {
        'form': form
        })
# Create your views here.
