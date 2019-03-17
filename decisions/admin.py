from django.contrib import admin
from .models import Course
from module0.admin import Module0
from module1.admin import Module1
from module2.admin import Module2
from module3.admin import Module3


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    readonly_fields = ('user',)
    list_display = ('__str__','user_details', 'module0', 'module1', 'module2')
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        if len(self.readonly_fields) > 0:
            return list(self.readonly_fields) + \
                   [field.name for field in obj._meta.fields] + \
                   [field.name for field in obj._meta.many_to_many]
        else:
            return list()

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

    def module0(self, course):
        return self.module(Module0, course)
    module0.allow_tags = True

    def module1(self, course):
        return self.module(Module1, course)
    module1.allow_tags = True

    def module2(self, course):
        return self.module(Module2, course)
    module2.allow_tags = True

    def module3(self, course):
        return self.module(Module3, course)
    module3.allow_tags = True
