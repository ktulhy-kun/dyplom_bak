# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-19 18:36
from __future__ import unicode_literals

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='MyNsuUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=300), size=None)),
                ('first_name', models.CharField(default='', max_length=100)),
                ('last_name', models.CharField(default='', max_length=100)),
                ('patronymic', models.CharField(default='', max_length=100)),
                ('sex', models.SmallIntegerField(choices=[(0, 'Unknown'), (1, 'Woman'), (2, 'Man')])),
                ('group', models.CharField(max_length=20)),
                ('faculty', models.CharField(max_length=20)),
                ('course', models.CharField(max_length=30)),
                ('user_type', models.CharField(max_length=80)),
                ('leave', models.BooleanField(default=False)),
                ('foreign', models.BooleanField(default=False)),
                ('qualification', models.CharField(max_length=80)),
            ],
        ),
    ]