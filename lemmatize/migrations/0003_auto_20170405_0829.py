# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 08:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lemmatize', '0002_lemmameet_post'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lemmameet',
            name='date',
        ),
        migrations.AddField(
            model_name='lemmameet',
            name='timestamp',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
