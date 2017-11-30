from django.contrib import admin
from .models import Course, Module1, Module2


@admin.register(Module1)
class Module1Admin(admin.ModelAdmin):
    list_display = ('course', 'completed_on', 'step',
                    'cc0', 'cc1', 'cc2', 'decision', 'cc', 'cc_not')
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]


@admin.register(Module2)
class Module2Admin(admin.ModelAdmin):
    list_display = ('course', 'completed_on', 'step',
                    'nylah_bias', 'evidence0', 'evidence1', 'evidence2')
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]


class Module1Inline(admin.StackedInline):
    model = Module1


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)
    list_display = ('__str__','module1','module2')
    inlines = [
        Module1Inline,
    ]
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

    def module1(self, course):
        module = Module1.objects.filter(course=course).first()
        if not module:
            return ''
        return module.step

    def module2(self, course):
        module = Module2.objects.filter(course=course).first()
        if not module:
            return ''
        return module.step

