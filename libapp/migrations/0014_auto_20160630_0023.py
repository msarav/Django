# -*- coding: utf-8 -*-
# Generated by Django 1.9.7 on 2016-06-30 00:23
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('libapp', '0013_auto_20160629_2316'),
    ]

    operations = [
        migrations.AlterField(
            model_name='libitem',
            name='date_acquired',
            field=models.DateField(default=datetime.date(2016, 6, 30)),
        ),
    ]