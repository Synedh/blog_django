# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-13 12:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='author',
            field=models.CharField(default='', max_length=1024),
            preserve_default=False,
        ),
    ]
