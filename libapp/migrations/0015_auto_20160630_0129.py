# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-30 01:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libapp', '0014_auto_20160630_0023'),
    ]

    operations = [
        migrations.AddField(
            model_name='suggestion',
            name='author',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='edition',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='suggestion',
            name='publication',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
