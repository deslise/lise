# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-29 00:19
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('managedata', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemTopic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noun', models.CharField(max_length=50)),
            ],
        ),
        migrations.RemoveField(
            model_name='topic',
            name='opinion',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='relations_topics',
        ),
        migrations.AddField(
            model_name='categorybusiness',
            name='active',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='opinion',
            name='topics',
            field=models.ManyToManyField(blank=True, null=True, to='managedata.Topic'),
        ),
        migrations.AddField(
            model_name='topic',
            name='description',
            field=models.CharField(default='', max_length=240),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='topic',
            name='topic',
            field=models.CharField(max_length=50),
        ),
        migrations.AddField(
            model_name='itemtopic',
            name='categories',
            field=models.ManyToManyField(to='managedata.CategoryBusiness'),
        ),
        migrations.AddField(
            model_name='itemtopic',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itemtopics', to='managedata.Topic'),
        ),
    ]
