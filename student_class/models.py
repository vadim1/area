from __future__ import unicode_literals

from django.db import models
from decisions.models import Course, User


class StudentClass(models.Model):
    instructor = models.ForeignKey(User, null=True)
    created_on = models.DateField(auto_now_add=True, blank=True)
    starting_module = models.IntegerField(default=0)
    completed_on = models.DateField(null=True)

    def __str__(self):
        to_return = ''
        if self.completed_on:
            to_return = "Closed "
        to_return += "Module " + str(self.starting_module) + " Class by " + str(self.instructor.get_short_name())
        return to_return

    class Meta:
        verbose_name = 'Class'
        verbose_name_plural = 'Classes'

    @staticmethod
    def create(instructor, module):
        student_class = StudentClass()
        student_class.instructor = instructor
        student_class.starting_module = module
        student_class.save()
        return student_class

    def add_student(self, student):
        student_class_student = StudentClassStudent()
        student_class_student.student_class = self
        courses = Course.objects.filter(user=student)
        # TODO: Handle no course
        student_class_student.course = courses[0]  # TODO: Add support for multiple courses
        student_class_student.save()
        return student_class_student

    def students(self):
        return StudentClassStudent.objects.filter(student_class=self)

    """
    Get all currently open classes, excluding those already joined by "course" if passed in
    """
    @staticmethod
    def open_classes(course=None):
        open_class_list = StudentClass.objects.filter(completed_on=None)
        if course:
            open_class_list = open_class_list.exclude(studentclassstudent__course=course)
        return open_class_list

    @staticmethod
    def my_classes(course):
        classes = []
        scsc = StudentClassStudent.objects.filter(course=course)
        for scs in scsc:
            classes.append(scs.student_class)
        return scsc


class StudentClassStudent(models.Model):
    student_class = models.ForeignKey(StudentClass, null=False)
    course = models.ForeignKey(Course, null=False)
    joined_on = models.DateField(auto_now_add=True, blank=True)
    current_module = models.IntegerField(null=True)
    left_on = models.DateField(null=True)

    def __str__(self):
        to_return = str(self.student_class)
        return to_return

    class Meta:
        verbose_name = 'Class Student'
        verbose_name_plural = 'Class Students'
