from __future__ import unicode_literals

from django.db import models
from accounts.models import User


class Problem(models.Model):
    user = models.ForeignKey(User)
    decision_type = models.CharField(max_length=255)
    decision = models.CharField(max_length=255)
    options = models.CharField(max_length=255)
    time_frame = models.CharField(max_length=255)
    decision_type_other = models.CharField(max_length=255)
    success = models.CharField(max_length=255)


class Question(models.Model):
    problem = models.ForeignKey(Problem)
    answer = models.CharField(max_length=50)
