# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-22 08:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0012_profile_twitter_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(blank=True, default='media/login-icon.png', null=True, upload_to='media'),
        ),
    ]
