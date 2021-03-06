# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-02-10 16:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('area_app', '0002_auto_20171007_1059'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='has_tou',
            field=models.BooleanField(default=False, help_text='Designates whether user sees the Terms of Use message.', verbose_name='terms of use'),
        ),
    ]
