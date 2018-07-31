from django.contrib import admin
from .models import Course, Module2


@admin.register(Module2)
class Module2Admin(admin.ModelAdmin):
    list_display = ('course', 'completed_on', 'step', 'nylah_bias',
                    'fact0', 'source0', 'bias0',
                    'fact1', 'source1', 'bias1',
                    'fact2', 'source2', 'bias2',
                    )
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]
