# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-09-17 05:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module1', '0002_auto_20180917_0449'),
    ]

    operations = [
        migrations.AddField(
            model_name='module1',
            name='decision_as_question',
            field=models.CharField(default='', max_length=255),
        ),
    ]