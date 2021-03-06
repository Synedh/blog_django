# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-27 12:35
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_auto_20171026_1253'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=1024)),
            ],
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'ordering': ('pub_date',)},
        ),
        migrations.AddField(
            model_name='tag',
            name='post',
            field=models.ManyToManyField(to='posts.Post'),
        ),
    ]
