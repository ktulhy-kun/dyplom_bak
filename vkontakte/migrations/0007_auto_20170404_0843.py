# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-04 08:43
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vkontakte', '0006_auto_20170404_0620'),
    ]

    operations = [
        migrations.AddField(
            model_name='vkgroup',
            name='name',
            field=models.CharField(default='', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='vkgroup',
            name='row',
            field=django.contrib.postgres.fields.jsonb.JSONField(default={}),
            preserve_default=False,
        ),
    ]
