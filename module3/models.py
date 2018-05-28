from __future__ import unicode_literals

from django.db import models
from decisions.models import Course


class Module3(models.Model):
    course = models.ForeignKey(Course)
    completed_on = models.DateField(null=True)
    step = models.CharField(max_length=20, default='')
    answers = models.TextField(default='')

    @staticmethod
    def num():
        return 3

    @staticmethod
    def name():
        return 'Absolute'

    def __str__(self):
        to_return = "Module 3: " + self.name()
        ro_return = to_return + " step " + self.step
        if self.completed_on:
            to_return = to_return + " completed on " + str(self.completed_on)
        return to_return

    class Meta:
        verbose_name = 'Module 3 Data'
        verbose_name_plural = 'Module 3 Data'
