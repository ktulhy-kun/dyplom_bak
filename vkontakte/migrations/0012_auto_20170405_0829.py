# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 08:29
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vkontakte', '0011_remove_vkpost_date'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vkpost',
            old_name='_date',
            new_name='timestamp',
        ),
    ]
