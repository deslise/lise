# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-14 17:10
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('liseapp', '0005_auto_20171208_2148'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 14, 17, 10, 20, 401985)),
        ),
    ]
