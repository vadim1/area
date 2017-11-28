from __future__ import unicode_literals

from django.db import models
from area_app.models import User


class Course(models.Model):
    user = models.ForeignKey(User, null=True)
    intro_on = models.DateField(null=True)


class Module1(models.Model):
    course = models.ForeignKey(Course)
    completed_on = models.DateField(null=True)
    step = models.CharField(max_length=20, default='')
    answers = models.TextField(default='')
    cc0 = models.CharField(max_length=255, default='')
    cc1 = models.CharField(max_length=255, default='')
    cc2 = models.CharField(max_length=255, default='')
    decision = models.CharField(max_length=255, default='')
    cc = models.CharField(max_length=255, default='')
    cc_not = models.CharField(max_length=255, default='')
    decision_buddy = models.CharField(max_length=80, default='')
    decision_buddy_email = models.EmailField(max_length=80, default='')


class Module2(models.Model):
    course = models.ForeignKey(Course)
    completed_on = models.DateField(null=True)
    step = models.CharField(max_length=20, default='')
    answers = models.TextField(default='')
    biases = models.TextField(default='')
    nylah_bias = models.CharField(max_length=40, default='')
    evidence0 = models.CharField(max_length=255, default='')
    evidence1 = models.CharField(max_length=255, default='')
    evidence2 = models.CharField(max_length=255, default='')
