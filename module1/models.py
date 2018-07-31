from __future__ import unicode_literals

from django.db import models
from decisions.models import Course, BaseModule


class Module1(BaseModule):
    answers = models.TextField(default='')
    cc0 = models.CharField(max_length=255, default='')  # Nylah
    cc1 = models.CharField(max_length=255, default='')  # Nylah
    cc2 = models.CharField(max_length=255, default='')  # Nylah
    decision = models.CharField(max_length=255, default='')
    cc = models.CharField(max_length=255, default='')
    cc_not = models.CharField(max_length=255, default='')
    decision_buddy = models.CharField(max_length=80, default='')
    decision_buddy_email = models.EmailField(max_length=80, default='')

    @staticmethod
    def num():
        return 1

    @staticmethod
    def name():
        return 'Introduction to Decision Making'

    def __str__(self):
        to_return = "Module 1 step " + self.step
        if self.completed_on:
            to_return = to_return + " completed on " + str(self.completed_on)
        return to_return

    class Meta:
        verbose_name = 'Module 1 Data'
        verbose_name_plural = 'Module 1 Data'
