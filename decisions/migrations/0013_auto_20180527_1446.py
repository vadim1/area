# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2018-05-27 14:46
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('decisions', '0012_auto_20180527_1414'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studentclass',
            name='instructor',
        ),
        migrations.RemoveField(
            model_name='studentclassstudent',
            name='course',
        ),
        migrations.RemoveField(
            model_name='studentclassstudent',
            name='student_class',
        ),
        migrations.DeleteModel(
            name='StudentClass',
        ),
        migrations.DeleteModel(
            name='StudentClassStudent',
        ),
    ]