from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm
from django.utils.html import format_html_join
from simple_history.models import HistoricalRecords

from area_app.models import QuestionModel
from decisions.models import Course, BaseModule

import ast
import json
import re

class Module0(BaseModule):
    answers = models.TextField(default='')
    archetype = models.CharField(max_length=20, default='')
    psp_correct = models.CharField(max_length=20, default='')
    work_on = models.CharField(max_length=255, default='')
    other_archetypes = models.TextField(default='')
    cheetah_answers = models.TextField(default='')

    # For the time being only save the cheetah sheet answers
    # If you have to add/remove fields from this list, make sure to re-run
    # ./manage.py makemigrations && ./manage.py migrate to update the history model
    excluded_fields = [
        'step',
        'completed_on',
        'answers',
        'archetype',
        'psp_correct',
        'work_on',
        'other_archetypes',
    ]
    history = HistoricalRecords(excluded_fields=excluded_fields)

    def save_without_historical_record(self, *args, **kwargs):
        self.skip_history_when_saving = True
        try:
            ret = self.save(*args, **kwargs)
        finally:
            del self.skip_history_when_saving
        return ret

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
        return 'The Problem Solver Profile'

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

    @staticmethod
    def load_json(json_data):
        json_object = {}
        try:
            json_object = json.loads(json_data)
        except Exception as e:
            if hasattr(e, 'message'):
                print(e.message)
            else:
                print(e)

        return json_object

    # List of all PSP profiles
    def profiles(self):
        profiles = [
            { 'id': 'adventurer', 'what': 'trust your gut & follow your passions' },
            { 'id': 'detective', 'what': 'track down clues & gather the evidence' },
            { 'id': 'listener', 'what': "consider others' points of view" },
            { 'id': 'thinker', 'what': 'examine possibilities before diving in' },
            { 'id': 'visionary', 'what': 'come up with solutions not tried before'},
        ]

        return profiles

    def __str__(self):
        to_return = "Module {} step {}".format(self.display_num, self.step)
        if self.completed_on:
            to_return = to_return + " completed on " + str(self.completed_on)
        return to_return

    def init_cheetah_answers(self):
        return '[{"id": 1, "answers": [ "", ""]},{"id": 2, "answers": [ "", ""]},{"id": 3, "answers": [ "", ""]},{"id": 4, "answers": [ "", ""]}]'

    @staticmethod
    def pins():
        pins = [
            'Your Decision-Making Preferences',
            'Your PSP',
            'Strengths and Blind Spots',
            'All PSPs',
        ]

        return pins

    class Meta:
        verbose_name = "Module 1 Data - Problem Solver Profile"
        verbose_name_plural = "Module 1 Data - Problem Solver Profile"

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

class Module0Form(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Module0Form, self).__init__(*args, **kwargs)
        # Not all fields are available all at once so set these to false for now
        self.fields['answers'].required = False
        self.fields['archetype'].required = False
        self.fields['cheetah_answers'].required = False
        self.fields['other_archetypes'].required = False
        self.fields['psp_correct'].required = False
        self.fields['work_on'].required = False

    class Meta:
        model = Module0
        fields = [
            'answers',
            'archetype',
            'cheetah_answers',
            'other_archetypes',
            'psp_correct',
            'work_on',
        ]