# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-20 08:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0011_auto_20170920_0938'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='twitter_link',
            field=models.URLField(blank=True, max_length=50, null=True),
        ),
    ]
