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
    list_display = ('__str__','user_details', 'module1', 'module2')
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]

    def user_details(self, course):
        user = course.user
        return \
            "School: " + user.school + \
            "<br/>Dream Director: " + str(user.dream_director) + \
            "<br/>Grade: " + str(user.grade)
    user_details.allow_tags = True

    @staticmethod
    def module(model, course):
        this_module = model.objects.filter(course=course).first()
        if not this_module:
            return ""
        return '<a href="/admin/decisions/module' + str(model.num()) + '/' + str(this_module.id) + '">' + \
               str(this_module) + '</a>'

    def module1(self, course):
        return self.module(Module1, course)
    module1.allow_tags = True

    def module2(self, course):
        return self.module(Module2, course)
    module2.allow_tags = True

