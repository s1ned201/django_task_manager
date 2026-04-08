from django.contrib import admin
from task_manager.models import Tasks, Comments, ProjectDetails, Tags, Projects, Attachments
from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

# inline
class CommentInline(admin.TabularInline):
    model = Comments
    extra = 1

class TagInline(admin.TabularInline):
    model = Tags.tasks.through
    extra = 1
    # filter_horizontal = ('tasks',)

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
    list_display = (
        "display_name",
        "status",
        "priority",
        "project",
        "assignee",
        "priority_status"
    )
    list_display_links = ("display_name",)
    # list_display_links = ("name", "status")
    list_editable = ("status", "priority")
    readonly_fields = ("created_at",)
    list_filter = ("status","priority","project")
    inlines = (CommentInline, TagInline )
    def priority_status(self, obj):
        if obj.priority < 3:
            return "LOW"
        if obj.priority < 5:
            return "MEDIUM"
        return "HIGH"
    priority_status.string = ""
    priority_status.short_description = "Приоритет статуса"

    @admin.display(description='Наименование')
    def display_name(self, instance):
        return mark_safe(f"<h1>{instance.name}</h1>")


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






