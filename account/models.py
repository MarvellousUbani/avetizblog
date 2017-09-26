# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib.auth.models import User

from django.db import models

# Create your models here.

class Profile(models.Model):
	user=models.ForeignKey(User , null=True)
	address=models.CharField(max_length=200, null=True, blank=True)
	short_description=models.TextField(blank=True, null=True)
	phone=models.CharField(max_length=50, null=True, blank=True)
	cover_pic = models.ImageField(null=True, upload_to='media', blank=True)
	avatar=models.ImageField(null=True, upload_to='media', blank=True, default='media/login-icon.png')
	location = models.CharField(max_length=50, null=True, blank=True)
	country = models.CharField(max_length=50, null=True, blank=True)
	facebook_link = models.URLField(max_length=50, null=True, blank=True)
	twitter_link = models.URLField(max_length=50, null=True, blank=True)
	instagram_link = models.URLField(max_length=50, null=True, blank=True)
	linkedin_link = models.URLField(max_length=50, null=True, blank=True)
	role=models.CharField(null=True, max_length=50, blank=True, default='Content Writer' , choices=(('Advertiser', 'Advertiser'), 
																			('Content Writer', 'Content Writer'), 
																			('Social Media Executives', 'Social Media Executives'))
	                     )

	def __str__(self):
		return self.user.first_name


