from __future__ import unicode_literals

from django.db import models
from decisions.models import Course, BaseModule


class Module2(BaseModule):
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

    @staticmethod
    def name():
        return 'Cognitive Bias'

    def __str__(self):
        to_return = "Module 2 step " + self.step
        if self.completed_on:
            to_return = to_return + " completed on " + str(self.completed_on)
        return to_return

    class Meta:
        verbose_name = 'Module 2 Data'
        verbose_name_plural = 'Module 2 Data'
