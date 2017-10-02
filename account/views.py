# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import (authenticate,login as auth_login, logout as auth_logout)
from django.http import HttpResponseRedirect, Http404
from django.views.generic.edit import CreateView
from django.urls import reverse
from advert.models import Wallet
from .forms import LoginForm,UserCreateForm, ProfileForm, PasswordResetForm, PasswordForm
from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.conf import settings
from django.contrib import messages
from .models import Profile
from advert.models import Wallet
from django.views.generic.base import View
from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.contrib.auth.hashers import make_password
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
					profile=Profile.objects.get(user=user)
					request.session['role'] = profile.role
					request.session['img_url']=profile.avatar.url
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
	#form_class = UserCreateForm
	#template_name = "registration/register.html"

	def get(self, request):
		user_form=UserCreateForm()
		profile_form=ProfileForm()
		context={'user_form':user_form, 'profile_form':profile_form}
		return render(self.request, 'registration/register.html',context)


	def post(self,request, *args, **kwargs):
		form=UserCreateForm(request.POST)
		profile_form=ProfileForm(request.POST)
		
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
			role=self.request.POST['role']

			try:
				user=User(first_name=firstname, email=email,username=username, is_staff=False,password=password, is_active=True)
				user.save()
				profile=Profile(user=user,role=role).save()
				wallet=Wallet(Owner=user).save()
				messages.success(self.request, 'SignUp Successful.Please login now')
				return HttpResponseRedirect(reverse('account:login', current_app='account'))
			except:
				return render(self.request, 'registration/register.html', {'user_form':UserCreateForm(request.POST), 'username':'Username already exist'})
		else:
			return render(self.request,'registration/register.html', {'user_form':UserCreateForm(request.POST), 'capcha':'capcha error'})


	def form_invalid(self,form):
		return render(self.request, 'registration/register.html', {'user_form': form})

class PasswordResetView(View):
	
	def post(self, request, *args, **kwargs):
		unique_id = get_random_string(length=32)
		form=PasswordResetForm(self.request.POST)
		if form.is_valid():
			username=form.cleaned_data['username']
			try:
				user=User.objects.get(username=username)
			except ObjectDoesNotExist:
				messages.warning(self.request, 'Username not registered. Please Sign Up ')
				return HttpResponseRedirect(reverse('account:signup'))

			try:
				profile=Profile.objects.get(user=user)
			except ObjectDoesNotExist:
				messages.warning(self.request, 'Username not registered. Please Sign Up ')
				return HttpResponseRedirect(reverse('account:signup'))
				
			profile.password_token=unique_id
			profile.save()
			message = render_to_string('advert/includes/password_reset_email.html', {
                
                'token':unique_id,
                'username':user.username,
            })
	        messages.success(self.request, 'We have sent a password reset link to your  email address . Thank You ')
	        mail_subject = 'Change Password.'
	        email = EmailMessage(mail_subject, message,'contact@avetiz.com', to=[user.email], reply_to=['contact@avetiz.com'],)
	        email.send()
	        return HttpResponseRedirect(reverse('account:login'))

class PasswordChangeView(View):
	def get(self,request, *args,**kwargs):
		token=self.request.GET.get('token')
		username=self.request.GET.get('username')
		#pdb.set_trace()
		user=get_object_or_404(User,username=username)
		profile=get_object_or_404(Profile, user=user)
		if profile.password_token == token:
			self.request.session['username']=username
			profile.password_token='abc098'
			profile.save()
			return render(self.request,'registration/password_set_form.html', {'form':PasswordForm()})

		else:
			raise Http404('Invalid Request')

	def post(self,request, *args, **kwargs):
		form=PasswordForm(self.request.POST)
		if form.is_valid():
			password=form.cleaned_data['password']
			user=get_object_or_404(User,username=self.request.session['username'])
			hashpassword=make_password(password)
			user.password=hashpassword
			user.save()
			messages.success(self.request, 'Password Change Successful ')
			return HttpResponseRedirect(reverse('account:login'))










		




				
		