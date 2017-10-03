# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-02 14:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0016_profile_password_token'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='account_name',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='account_number',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='bank_name',
            field=models.CharField(max_length=200, null=True),
        ),
    ]