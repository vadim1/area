from django.contrib import admin
from .models import Course, Module0

@admin.register(Module0)
class Module0Admin(admin.ModelAdmin):
    list_display = ('course', 'completed_on', 'step',
                    'archetype', 'display_other_archetypes', 'psp_correct')
    readonly_fields = []
    # Do not display work_on
    # In the module0 refactor its not being referenced
    # TODO: Perhaps we should just get rid of this in the future
    exclude = ('work_on',)
