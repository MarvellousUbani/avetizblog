# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-30 16:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0014_auto_20170926_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='media/login-icon.png', null=True, upload_to='media'),
        ),
    ]
