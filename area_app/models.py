from __future__ import unicode_literals

from django.db import models


class UserProfile(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    facebook_username = models.CharField(max_length=255)
    email = models.EmailField()


class Problem(models.Model):
    user = models.ForeignKey(UserProfile)
    decision_type = models.CharField(max_length=255)
    decision = models.CharField(max_length=255)
    options = models.CharField(max_length=255)
    time_frame = models.CharField(max_length=255)
    decision_type_other = models.CharField(max_length=255)
    success = models.CharField(max_length=255)


class Question(models.Model):
    problem = models.ForeignKey(Problem)
    answer = models.CharField(max_length=50)
