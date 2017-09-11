# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class advertPlan(models.Model):
	name=models.CharField(max_length=50)
	frequency=models.CharField(max_length=50, choices=(('Weekly','Weekly'),('Daily','Daily'),('Monthly','Monthly')))
	cost=models.IntegerField()
	page=models.CharField(max_length=50,choices=(('home','home'),('detail','detail')))

	def __str__(self):
		return self.name



class Advert(models.Model):
	company=models.CharField(max_length=70)
	advert_banner=models.ImageField(upload_to='media')
	advert_desc=models.TextField()
	duration=models.IntegerField()
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








#pk_test_d7ed8771f755bc62d8d023a93e531101a3ac4eb8





