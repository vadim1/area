from __future__ import unicode_literals

from django.db import models
from area_app.models import User
from area_app.models import QuestionModel


class Course(models.Model):
    user = models.ForeignKey(User, null=True)
    intro_on = models.DateField(null=True)

    def __str__(self):
        return "FP: " + str(self.user)

    class Meta:
        verbose_name = "Course Taker"

    @staticmethod
    def load_course(request):
        course = None
        if request.user.is_authenticated():
            courses = Course.objects.filter(user=request.user)
            if courses:
                course = courses.first()
            else:
                course = Course(user=request.user)
                course.save()
        return course

    @staticmethod
    def num_modules():
        return 4


class Module0(models.Model):
    course = models.ForeignKey(Course)
    completed_on = models.DateField(null=True)
    step = models.CharField(max_length=20, default='')
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
        to_return = "Module 0 "
        ro_return = to_return + " step " + self.step
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


class Module1(models.Model):
    course = models.ForeignKey(Course)
    completed_on = models.DateField(null=True)
    step = models.CharField(max_length=20, default='')
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

    @staticmethod
    def name():
        return 'Cognitive Bias'

    def __str__(self):
        to_return = "Module 2 "
        ro_return = to_return + " step " + self.step
        if self.completed_on:
            to_return = to_return + " completed on " + str(self.completed_on)
        return to_return

    class Meta:
        verbose_name = 'Module 2 Data'
        verbose_name_plural = 'Module 2 Data'
