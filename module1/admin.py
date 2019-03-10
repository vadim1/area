from django.contrib import admin
from .models import Course, Module1


@admin.register(Module1)
class Module1Admin(admin.ModelAdmin):
    list_display = ('course', 'completed_on', 'step',
                    'decision', 'cc', 'cc_not')
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        if len(self.readonly_fields) > 0:
            return list(self.readonly_fields) + \
                   [field.name for field in obj._meta.fields] + \
                   [field.name for field in obj._meta.many_to_many]
        else:
            return list()


class Module1Inline(admin.StackedInline):
    model = Module1
