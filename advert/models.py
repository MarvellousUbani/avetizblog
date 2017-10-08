# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.http import JsonResponse, HttpResponseRedirect
from blog.models import Post
from django.db.models import Q
from django.urls import reverse

# Create your models here.
class advertPlan(models.Model):
	name=models.CharField(max_length=50, null=True)
	cost=models.IntegerField(null=True)
	
	def __str__(self):
		return self.name


class Duration(models.Model):
	plan=models.ForeignKey(advertPlan)
	name=models.CharField(max_length=50, choices=(('1 Week', '1 Week'), ('1 Month', '1 Month'),('Quaterly', 'Quaterly'), ('Anually', 'Anually')))
	price=models.IntegerField()

	def __str__(self):
		return self.name

class Advert(models.Model):
	company=models.CharField(max_length=70)
	advert_banner=models.ImageField(upload_to='media')
	advert_desc=models.TextField()
	duration=models.CharField(max_length=50,null=True, choices=(('1 Week', '1 Week'), ('1 Month', '1 Month'),('Quaterly', 'Quaterly'), ('Anually', 'Anually')))
	status=models.BooleanField(default=False)
	publisher=models.ForeignKey(User, null=True)
	payt_status=models.BooleanField(default=False)
	created_on=models.DateField(auto_now=True)
	plan=models.ForeignKey(advertPlan, null=True)
	advert_cost=models.IntegerField(null=True)
	link=models.URLField(null=True)

	def __str__(self):
		return self.company

	def approve(self):
		self.status=True
		return True

	def setUp(self, user):
		self.advert_cost= self.duration*self.plan.cost
		self.publisher=user
		return True


class Wallet(models.Model):
	Owner=models.OneToOneField(User, on_delete=models.CASCADE)
	amount=models.IntegerField(null=True, blank=True, default="0")

class Transaction(models.Model):
	amount=models.IntegerField()
	date=models.DateTimeField(auto_now=True)
	description=models.CharField(max_length=100)
	trans_type=models.CharField(max_length=50, choices=(('Credit','Credit'),('Debit', 'Debit')))
	wallet=models.ForeignKey(Wallet)
	status=models.CharField(max_length=20, choices=(('Pending','Pending'),("Completed",'Completed')))
	ref=models.CharField(max_length=20, null=True)

	def approve(self):
		self.status='Completed'
		self.wallet.amount+=self.amount
		self.save()
		self.wallet.save()



class Report(models.Model):
	rfrom=models.DateField()
	rto=models.DateField()
	user=models.ForeignKey(User)
	status=models.CharField(max_length=90, choices=(('Sent', 'Sent'), ('Not Sent','Not Sent')), default='Not Sent')
	created_date=models.DateField(auto_now_add=True, null=True)
	description=models.TextField(null=True)

	def setUp(self, user):
		self.user=user 
		self.save()

	def send(self, request):
		posts=Post.objects.filter(Q(created_date__gte= self.rfrom), created_date__lte=self.rto).filter(author=request.user)
		
		count=posts.count()
		context = {'report': self, 'posts': posts, 'count':count, 'username':request.user.username}
		message = render_to_string('advert/includes/partial_report_view.html',context)
		
		mail_subject = 'Report from '+ request.user.username
		email = EmailMessage(mail_subject, message,'contact@avetiz.com', to=['tolu.akano@avetiz.com'], reply_to=['contact@avetiz.com'],)
		email.content_subtype = "html" 
		try:
			messages.success(request, 'Your Report has been sent . Thank You ')
			email.send()
			self.status='Sent'
		except:
			messages.warning(request, 'Your Report was not sent. Please try again ')	
		
		self.save()
		return HttpResponseRedirect(reverse('advert:report'))
		











#pk_test_d7ed8771f755bc62d8d023a93e531101a3ac4eb8





