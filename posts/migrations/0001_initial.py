# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-13 10:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Commentary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.CharField(max_length=1024)),
                ('content', models.CharField(max_length=32768)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=1024)),
                ('content', models.CharField(max_length=32768)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
    ]
