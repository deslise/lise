# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-14 17:44
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liseapp', '0007_auto_20171214_1721'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 14, 17, 44, 15, 71571)),
        ),
    ]
