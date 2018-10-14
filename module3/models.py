from __future__ import unicode_literals

from django.db import models
from decisions.models import Course, BaseModule


class Module3(BaseModule):
    answers = models.TextField(default='')

    @staticmethod
    def num():
        return 3

    # Used to display the number to the user
    # internally it's still module 0
    @staticmethod
    def display_num():
        return 4

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
