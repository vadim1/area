from __future__ import unicode_literals

from django.db import models
from area_app.models import QuestionModel
from decisions.models import Course, BaseModule


class Module0(BaseModule):
    answers = models.TextField(default='')
    archetype = models.CharField(max_length=20, default='')
    psp_correct = models.CharField(max_length=20, default='')
    work_on = models.CharField(max_length=255, default='')

    @staticmethod
    def num():
        return 0

    @staticmethod
    def name():
        return 'Problem Solver Profile'

    def __str__(self):
        to_return = "Module 0 step " + self.step
        if self.completed_on:
            to_return = to_return + " completed on " + str(self.completed_on)
        return to_return

    class Meta:
        verbose_name = 'Module 0 Data'
        verbose_name_plural = 'Module 0 Data'


class Question(models.Model):
    module0 = models.ForeignKey(Module0)
    question = models.ForeignKey(QuestionModel, related_name='module0_question', null=True)
    answer = models.BooleanField(default=False)

    @staticmethod
    def get_yes_questions(user):
        yes_questions_query = Question.objects.filter(user=user, answer=True)
        return yes_questions_query.all()

    @staticmethod
    def fill_in_user(user, session_key):
        Question.objects.filter(session_key__exact=session_key, user__isnull=True).update(user=user)

    def text(self):
        return self.question.text()
