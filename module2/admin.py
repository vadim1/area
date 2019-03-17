from django.contrib import admin
from .models import Course, Module2


@admin.register(Module2)
class Module2Admin(admin.ModelAdmin):
    list_display = ('course', 'completed_on', 'step',
                    )
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        if len(self.readonly_fields) > 0:
            return list(self.readonly_fields) + \
                   [field.name for field in obj._meta.fields] + \
                   [field.name for field in obj._meta.many_to_many]
        else:
            return list()
