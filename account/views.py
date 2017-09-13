# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect
from django.contrib.auth import (authenticate,login as auth_login, logout as auth_logout)
from django.http import HttpResponseRedirect
from django.views.generic.edit import CreateView
from django.urls import reverse
from advert.models import Wallet
from .forms import LoginForm,UserCreateForm
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib import messages
from .models import Profile
import urllib
import urllib2
import json
import pdb
# Create your views here.
def login(request):
	message=''
	if request.user.is_authenticated():
			
		return HttpResponseRedirect(reverse('advert:dashboard', current_app='advert'))
	if request.method == "POST":
		form=LoginForm(request.POST)
		if form.is_valid():
			_username=form.cleaned_data['username']
			_password=form.cleaned_data['password']
			user=authenticate(username=_username, password=_password)
			if user is not None:
				if user.is_active:
					auth_login(request, user)
					if request.GET.get('next'):
						return redirect(request.GET.get('next'))
					else:
					    return HttpResponseRedirect(reverse('advert:dashboard', current_app='advert'))
				else:
					message = 'Your account is not activated'
			else:
				message = 'Username or password wrong. Please try again.'
	form=LoginForm()			
	context = {'message': message, 'form':form}


	return render(request, 'registration/login.html', context)

def logout(request):
	if request.user.is_authenticated():
		auth_logout(request)
		return HttpResponseRedirect(reverse('account:login', current_app='account'))
	else:
		return HttpResponseRedirect(reverse('account:login', current_app='account'))

class SignUp(CreateView):
	form_class = UserCreateForm
	template_name = "registration/register.html"

	def post(self,request, *args, **kwargs):
		form=UserCreateForm(request.POST)
		
		''' Begin reCAPTCHA validation '''
		
		recaptcha_response = request.POST.get('g-recaptcha-response')
		url = 'https://www.google.com/recaptcha/api/siteverify'
		values = {
		    'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
		    'response': recaptcha_response
		}
		data = urllib.urlencode(values)
		req = urllib2.Request(url, data)
		response = urllib2.urlopen(req)
		result = json.load(response)
		''' End reCAPTCHA validation '''
		if result['success']:
			username=self.request.POST['username']
			email=self.request.POST['email']
			password=self.request.POST['password']
			password=make_password(password)
			firstname=self.request.POST['first_name']
			try:
				user=User(first_name=firstname, email=email,username=username, is_staff=False,password=password, is_active=True)
				user.save()
				profile=Profile(user=user).save()
				wallet=Wallet(Owner=user).save()
				return HttpResponseRedirect(reverse('account:login', current_app='account'))
			except:
				return render(self.request, 'registration/register.html', {'form':form, 'username':'Username already exist'})
		else:
			return render(self.request,'registration/register.html', {'form':form, 'capcha':'capcha error'})
		




				
		