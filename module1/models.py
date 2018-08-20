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
    cc1_list = models.TextField(default='')
    cc2_list = models.TextField(default='')
    living = models.TextField(default='')
    why_list = models.TextField(default='')

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
        return 'Introduction to Decision Making'

    @staticmethod
    def get_cc_list_answer(cc_list, ndx):
        if cc_list:
            return cc_list[ndx]
        else:
            return ""

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
    def get_why_options():
        why_options = [
            'Not sure how to solve my problem',
            'Worried I will make a poor decision',
            'Worried about what other people will think of my decision',
            'Not sure that I need to make the decision now',
        ]

        return why_options

    def __str__(self):
        to_return = "Module 1 step " + self.step
        if self.completed_on:
            to_return = to_return + " completed on " + str(self.completed_on)
        return to_return

    class Meta:
        verbose_name = 'Module 1 Data'
        verbose_name_plural = 'Module 1 Data'
