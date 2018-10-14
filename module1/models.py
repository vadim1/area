from __future__ import unicode_literals

from django.db import models
from django.forms import ModelForm
from simple_history.models import HistoricalRecords

from decisions.models import Course, BaseModule

class Module1(BaseModule):
    answers = models.TextField(default='')
    cc = models.TextField(default='')
    cc_not = models.CharField(max_length=255, default='')
    cc_occurred = models.TextField(default='')
    decision = models.CharField(max_length=255, default='')
    decision_as_question = models.CharField(max_length=255, default='')
    decision_buddy = models.CharField(max_length=80, default='')
    decision_buddy_email = models.EmailField(max_length=80, default='')
    living = models.TextField(default='')
    sample_cc = models.TextField(default='')
    practice_cc1 = models.TextField(default='')
    practice_cc2 = models.TextField(default='')
    why = models.TextField(default='')

    # For the time being only save the cheetah sheet answers
    # If you have to add/remove fields from this list, make sure to re-run
    # ./manage.py makemigrations && ./manage.py migrate to update the history model
    excluded_fields = [
        'step',
        'completed_on',
        'answers',
        'cc_not',
        'completed_on',
        'decision_buddy',
        'decision_buddy_email',
        'living',
        'sample_cc',
        'practice_cc1',
        'practice_cc2',
        'why',
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
        return 1

    # Used to display the number to the user
    # internally it's still module 0
    @staticmethod
    def display_num():
        return 2

    @staticmethod
    def name():
        return 'Introduction to Decision-Making'

    @staticmethod
    def get_cc_list_answer(cc_list, ndx):
        if cc_list:
            return cc_list[ndx]
        else:
            return ""

    @staticmethod
    def get_description():
        description = {
            '00': "Re-examine your process for outcomes you didn't like for routine matters",
            '01': "Use a process to keep routine matters from getting complicated",
            '10': "Replicate what you did for the ones you're happy, re-examine the rest",
            '11': "Gather data to help make these decisions",
        }

        return description

    @staticmethod
    def game1_questions():
        questions = {
            'Breakfast': 'What to eat for breakfast?',
            'Test': 'To study for a test or just hope for the best?',
            'Job': 'To get an internship or a summer job?',
            'Siblings': 'To take care of your siblings or meet up with friends?',
            'Netflix': 'To stay up watching Netflix or finish your homework?',
            'Lunch': 'Make lunch to bring in or buy at the cafeteria?',
            'Vegetarian': 'Eat meat or become a vegetarian?',
            'Action': 'Sit and wait or take action?',
            'Problem': 'Complain or fix the problem?',
            'Bullying': 'Watch someone get bullied or take action?',
            'Honesty': 'Be lied to or told the truth?',
            'College': 'Go to a 2-year college or a 4-year university?',
            'Coat': 'Wear a winter coat or just grab a sweatshirt?',
            'Hair': 'What to do with my hair?',
            'Friend': 'Share a problem with a friend?',
        }

        return questions

    @staticmethod
    def game_labels():
        labels = {
            'easy': ['Easy', 'Hard'],
            'confident': ['Confident', 'Unsure'],
        }

        return labels

    @staticmethod
    def get_what_changed():
        what_changed = [
            'Attainable',
            'Focused',
            'Realistic',
            'Short-sighted',
            'Unrelated',
            'Vague',
        ]

        return what_changed

    @staticmethod
    def get_why_options():
        why_options = [
            'Not sure how to solve my problem',
            'Worried I will make a poor decision',
            'Worried about what other people will think of my decision',
            'Not sure that I need to make the decision now',
        ]

        return why_options

    @staticmethod
    def pins():
        pins = [
            'Self-Awareness',
            'Your Vision of Success',
            'Confidence to Make Better Decisions',
        ]

        return pins

    def __str__(self):
        to_return = "Module 1 step " + self.step
        if self.completed_on:
            to_return = to_return + " completed on " + str(self.completed_on)
        return to_return

    class Meta:
        verbose_name = "Module 2 Data - Introduction to Decision-Making"
        verbose_name_plural = "Module 2 Data - Introduction to Decision-Making"

class Module1Form(ModelForm):
    def __init__(self, *args, **kwargs):
        super(Module1Form, self).__init__(*args, **kwargs)
        # Not all fields are available all at once so set these to false for now
        self.fields['answers'].required = False
        self.fields['cc'].required = False
        self.fields['cc_not'].required = False
        self.fields['cc_occurred'].required = False
        self.fields['decision'].required = False
        self.fields['decision_as_question'].required = False
        self.fields['decision_buddy'].required = False
        self.fields['decision_buddy_email'].required = False
        self.fields['living'].required = False
        self.fields['sample_cc'].required = False
        self.fields['practice_cc1'].required = False
        self.fields['practice_cc2'].required = False
        self.fields['why'].required = False

    class Meta:
        model = Module1
        fields = ['answers',
                  'cc',
                  'cc_not',
                  'cc_occurred',
                  'decision',
                  'decision_as_question',
                  'decision_buddy',
                  'decision_buddy_email',
                  'living',
                  'practice_cc1',
                  'practice_cc2',
                  'sample_cc',
                  'why'
                  ]