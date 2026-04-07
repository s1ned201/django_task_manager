from django.contrib import admin
from task_manager.models import Tasks, Comments, ProjectDetails, Tags, Projects, Attachments


# @admin.register(Tasks)
class TasksAdmin(admin.ModelAdmin):
    # fields = (('name', 'status'), 'description', 'priority')
    fieldsets = (
        ('Основная информация', {
            'fields': (
                ('name', 'status'),
            ),
            'description': 'Основные параметры задачи',
            'classes': ('wide',),
        }),
        ('Детальное описание', {
            'fields': ('description',),
            'description': 'Подробное описание задачи',
            'classes': ('wide', 'collapse'),
        }),
        ('Настройки приоритета', {
            'fields': ('priority',),
            'description': 'Установите приоритет выполнения задачи (1-10)',
            'classes': ('wide',),
        }),
    )
    exclude = ('is_reopened',)
    list_display = ("name", "status", "priority", "project", "assignee")
    list_display_links = ("name",)
    # list_display_links = ("name", "status")
    list_editable = ("status", "priority")
    readonly_fields = ("created_at",)
    list_filter = ("status","priority","project")


class ProjectsAdmin(admin.ModelAdmin):
    # fields = ('name', 'description')
    exclude = ('owner',)
    # list_display = ("name", "status", "priority", "project", "assignee")
    # list_display_links = ("name",)
    # # list_display_links = ("name", "status")
    # list_editable = ("status", "priority")
    # readonly_fields = ("created_at",)

admin.site.register(Tags)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(Comments)
admin.site.register(ProjectDetails)
admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Attachments)






