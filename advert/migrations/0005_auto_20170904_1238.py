# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-04 11:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advert', '0004_auto_20170904_1231'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='amount',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
