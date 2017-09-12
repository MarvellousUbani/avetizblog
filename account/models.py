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
	avatar=models.ImageField(null=True, upload_to='media', blank=True)

	def __str__(self):
		return self.user.first_name


