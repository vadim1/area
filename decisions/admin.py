from django.contrib import admin
from .models import Course, Module1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    pass


@admin.register(Module1)
class Module1Admin(admin.ModelAdmin):
    pass
