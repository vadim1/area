from django.contrib import admin
from .models import StudentClass


@admin.register(StudentClass)
class StudentClassAdmin(admin.ModelAdmin):
    list_display = ('instructor', 'created_on', 'students',)
    readonly_fields = []

    def get_readonly_fields(self, request, obj=None):
        return list(self.readonly_fields) + \
               [field.name for field in obj._meta.fields] + \
               [field.name for field in obj._meta.many_to_many]
