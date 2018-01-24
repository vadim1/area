from __future__ import unicode_literals

from django.db import models
from area_app.models import User


class Course(models.Model):
    user = models.ForeignKey(User, null=True)
    intro_on = models.DateField(null=True)

    def __str__(self):
        return "FP: " + str(self.user)

    class Meta:
        verbose_name = "Course Taker"


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

    @staticmethod
    def num():
        return 1

    def __str__(self):
        to_return = "Module 1 "
        ro_return = to_return + " step " + self.step
        if self.completed_on:
            to_return = to_return + " completed on " + str(self.completed_on)
        return to_return

    class Meta:
        verbose_name = 'Module 1 Data'
        verbose_name_plural = 'Module 1 Data'


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
    fact0 = models.CharField(max_length=255, default='')
    source0 = models.CharField(max_length=255, default='')
    bias0 = models.CharField(max_length=255, default='')
    fact1 = models.CharField(max_length=255, default='')
    source1 = models.CharField(max_length=255, default='')
    bias1 = models.CharField(max_length=255, default='')
    fact2 = models.CharField(max_length=255, default='')
    source2 = models.CharField(max_length=255, default='')
    bias2 = models.CharField(max_length=255, default='')

    @staticmethod
    def num():
        return 2

    def __str__(self):
        to_return = "Module 2 "
        ro_return = to_return + " step " + self.step
        if self.completed_on:
            to_return = to_return + " completed on " + str(self.completed_on)
        return to_return

    class Meta:
        verbose_name = 'Module 2 Data'
        verbose_name_plural = 'Module 2 Data'
