# -*- coding: utf-8 -*-
# Generated by Django 1.11.15 on 2018-10-06 16:40
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module1', '0004_auto_20181006_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='historicalmodule1',
            name='completed_on',
        ),
        migrations.RemoveField(
            model_name='historicalmodule1',
            name='step',
        ),
    ]
