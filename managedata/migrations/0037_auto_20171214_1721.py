# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-12-14 17:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('managedata', '0036_auto_20171214_1710'),
    ]

    operations = [
        migrations.AlterField(
            model_name='business',
            name='place_id',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]