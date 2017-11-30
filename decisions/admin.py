from django.contrib import admin
from .models import Course, Module1, Module2


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('__str__',)
    pass


@admin.register(Module1)
class Module1Admin(admin.ModelAdmin):
    list_display = ('course', 'completed_on', 'step',
                    'cc0', 'cc1', 'cc2', 'decision', 'cc', 'cc_not')
    pass


@admin.register(Module2)
class Module2Admin(admin.ModelAdmin):
    list_display = ('course', 'completed_on', 'step',
                    'nylah_bias', 'evidence0', 'evidence1', 'evidence2')
    pass
