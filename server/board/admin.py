from django.contrib import admin
from .models import Action, Node, Scenario, ScenarioAction


class NodeAdmin(admin.ModelAdmin):
    list_display = ('name', 'ip', 'is_active')
    list_editable = ('ip', 'is_active')


class ActionAdmin(admin.ModelAdmin):
    list_display = ('name', 'route', 'is_default')
    exclude = ('params',)
    ordering = ['-is_default']


class ScenarioActionsInline(admin.TabularInline):
    model = ScenarioAction
    extra = 0


class ScenarioAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ScenarioActionsInline]


admin.site.register(Node, NodeAdmin)
admin.site.register(Action, ActionAdmin)
admin.site.register(Scenario, ScenarioAdmin)
