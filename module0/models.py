from __future__ import unicode_literals

from django.db import models
from area_app.models import QuestionModel
from decisions.models import Course, BaseModule

import re

class Module0(BaseModule):
    answers = models.TextField(default='')
    archetype = models.CharField(max_length=20, default='')
    psp_correct = models.CharField(max_length=20, default='')
    work_on = models.CharField(max_length=255, default='')
    other_archetypes = models.TextField(default='')
    cheetah_answers = models.TextField(default='')

    @staticmethod
    def num():
        return 0

    # Used to display the number to the user
    # internally it's still module 0
    @staticmethod
    def display_num():
        return 1

    @staticmethod
    def name():
        return 'Problem Solver Profile'

    # The DB is in UTF-8 and the data are stored as text values in UTF-8
    # Utility is to convert to ASCII and strip out out any extraneous
    # characters
    @staticmethod
    def to_ascii(data, dataType=None):
        # https://stackoverflow.com/a/4299686
        udata = data.decode("utf-8")
        asciidata = udata.encode("ascii", "ignore")

        if dataType is None:
            asciidata = re.sub("\[u|\]", "", asciidata)
        elif dataType is 'JSON':
            asciidata = re.sub("\[u", "", asciidata)

        asciidata = re.sub("u'", "'", asciidata)
        asciidata = re.sub("u\"", "\"", asciidata)

        return (asciidata)

    def __str__(self):
        to_return = "Module 0 step " + self.step
        if self.completed_on:
            to_return = to_return + " completed on " + str(self.completed_on)
        return to_return

    def init_cheetah_answers(self):
        return '[{"id": 1, "answers": [ "", ""]},{"id": 2, "answers": [ "", ""]},{"id": 3, "answers": [ "", ""]},{"id": 4, "answers": [ "", ""]}]'

    def display_other_archetypes(self):
        asciidata = Module0.to_ascii(self.other_archetypes)
        # Strip out the [ and ]
        asciidata = re.sub("\[|\]", "", asciidata)

        other_archetypes = asciidata.split("), ")
        other_archetypes = [re.sub("\(|\)", "", x.strip()) for x in other_archetypes]

        # Add the newline
        other_archetypes = [x + "\n" for x in other_archetypes]

        return other_archetypes

    def display_answers(self):
        asciidata = Module0.to_ascii(self.answers)
        answers_list = asciidata.split(",")
        answers = [x.strip() for x in answers_list]

        return answers


    display_answers.short_description = "Answers"
    display_other_archetypes.short_description = "Other Archetypes"


    class Meta:
        verbose_name = 'Module 1 Data'
        verbose_name_plural = 'Module 1 Data'


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
