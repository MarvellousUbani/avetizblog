# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-07 08:52
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advert', '0021_auto_20171007_0945'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='description',
            field=models.TextField(null=True),
        ),
    ]
