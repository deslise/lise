# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-21 00:38
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('liseapp', '0020_auto_20171216_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='date',
            field=models.DateTimeField(default=datetime.datetime(2017, 12, 21, 0, 38, 31, 252131, tzinfo=utc)),
        ),
    ]
