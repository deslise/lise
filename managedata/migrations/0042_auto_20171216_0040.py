# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-16 00:40
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managedata', '0041_auto_20171215_2355'),
    ]

    operations = [
        migrations.AlterField(
            model_name='requestcategory',
            name='date_request',
            field=models.DateField(default=datetime.date(2017, 12, 16)),
        ),
        migrations.AlterField(
            model_name='review',
            name='review_id',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
