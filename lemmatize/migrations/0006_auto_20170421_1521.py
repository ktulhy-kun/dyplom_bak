# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-04-21 15:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lemmatize', '0005_lemma_source'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='lemma',
            name='source',
        ),
        migrations.AddField(
            model_name='lemmameet',
            name='source',
            field=models.CharField(default=' ', max_length=100),
            preserve_default=False,
        ),
    ]
