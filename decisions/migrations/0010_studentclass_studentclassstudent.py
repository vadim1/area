# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-05-27 10:43
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('decisions', '0009_auto_20180422_1248'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentClass',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_on', models.DateField()),
                ('starting_module', models.IntegerField()),
                ('completed_on', models.DateField(null=True)),
                ('instructor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Class',
                'verbose_name_plural': 'Classes',
            },
        ),
        migrations.CreateModel(
            name='StudentClassStudent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('joined_on', models.DateField()),
                ('current_module', models.IntegerField()),
                ('left_on', models.DateField(null=True)),
                ('course', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decisions.Course')),
                ('student_class', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='decisions.StudentClass')),
            ],
            options={
                'verbose_name': 'Class Student',
                'verbose_name_plural': 'Class Students',
            },
        ),
    ]
