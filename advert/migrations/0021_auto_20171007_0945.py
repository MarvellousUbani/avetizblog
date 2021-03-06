# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-10-07 08:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('advert', '0020_report'),
    ]

    operations = [
        migrations.AddField(
            model_name='report',
            name='created_date',
            field=models.DateField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='report',
            name='status',
            field=models.CharField(choices=[('Sent', 'Sent'), ('Not Sent', 'Not Sent')], default='Not Sent', max_length=90),
        ),
    ]
