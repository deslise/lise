# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-11-30 19:27
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('managedata', '0024_auto_20171130_1903'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'ordering': ['name']},
        ),
        migrations.AlterModelOptions(
            name='categorybusiness',
            options={'ordering': ['specialty']},
        ),
        migrations.AlterModelOptions(
            name='keyword',
            options={'ordering': ['keyword']},
        ),
    ]