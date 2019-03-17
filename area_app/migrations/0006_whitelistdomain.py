# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2019-03-10 22:06
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('area_app', '0005_auto_20190309_2235'),
    ]

    operations = [
        migrations.CreateModel(
            name='WhitelistDomain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain_name', models.CharField(blank=True, help_text='Email domain to whitelist', max_length=256, null=True)),
                ('access_override', models.BooleanField(default=False, help_text='When true, ignore the max limit')),
                ('max_limit', models.IntegerField(default=3, help_text='Maximum access limit per user')),
                ('is_active', models.BooleanField(default=True, help_text='Is this whitelist rule active?')),
            ],
        ),
    ]
