# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-04 06:09
from __future__ import unicode_literals

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vkontakte', '0003_vkuser_faculty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='vkpost',
            name='source',
        ),
        migrations.AddField(
            model_name='vkpost',
            name='source_data',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=None),
            preserve_default=False,
        ),
    ]