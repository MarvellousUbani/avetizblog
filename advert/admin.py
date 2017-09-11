# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Wallet, Transaction, Advert, advertPlan

# Register your models here.
admin.site.register(Wallet)
admin.site.register(Transaction)
admin.site.register(Advert)
admin.site.register(advertPlan)
