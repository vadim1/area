from django.contrib import admin
from .models import Course, Module0


@admin.register(Module0)
class Module0Admin(admin.ModelAdmin):
    list_display = ('course', 'completed_on', 'step',
                    'archetype', 'psp_correct', 'work_on')
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]
