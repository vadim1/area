from __future__ import unicode_literals

from django.db import models
from area_app.models import User


class Course(models.Model):
    user = models.ForeignKey(User, null=True)
    intro_on = models.DateField(null=True)
    current_module = models.IntegerField(null=False, default=0)

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

    def page(self, module_class):
        module = module_class.objects.get(course=self)
        if module:
            return module.step
        else:
            return ''


class BaseModule(models.Model):
    course = models.ForeignKey(Course)
    completed_on = models.DateField(null=True)
    step = models.CharField(max_length=20, default='')

    class Meta:
        abstract = True
