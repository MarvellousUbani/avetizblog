# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-09-16 16:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('advert', '0016_auto_20170916_1648'),
    ]

    operations = [
        migrations.CreateModel(
            name='Duration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('1 Week', '1 Week'), ('1 Month', '1 Month'), ('Quaterly', 'Quaterly'), ('Anually', 'Anually')], max_length=50)),
                ('price', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='advertplan',
            name='description',
        ),
        migrations.RemoveField(
            model_name='advertplan',
            name='frequency',
        ),
        migrations.RemoveField(
            model_name='advertplan',
            name='price',
        ),
        migrations.AddField(
            model_name='advertplan',
            name='cost',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='duration',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='advert.advertPlan'),
        ),
        migrations.AddField(
            model_name='advert',
            name='duration',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='advert.Duration'),
        ),
    ]