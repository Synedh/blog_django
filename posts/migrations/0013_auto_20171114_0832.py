# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-14 08:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0012_option_used'),
    ]

    operations = [
        migrations.AddField(
            model_name='option',
            name='name',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='option',
            name='message',
            field=models.CharField(default='', max_length=256),
        ),
    ]
