from django.contrib import admin
from task_manager.models import Tasks, Comments, ProjectDetails, Tags, Projects, Attachments
# from django.utils.html import format_html_join
from django.utils.safestring import mark_safe

"""
INLINE
"""
class CommentInline(admin.TabularInline):
    model = Comments
    extra = 1

class TagInline(admin.TabularInline):
    model = Tags.tasks.through
    extra = 1
    # filter_horizontal = ('tasks',)

class ProjectDetailsInLine(admin.StackedInline):
    model = ProjectDetails
    extra = 1

"""
ACTION
"""
@admin.action(description="Переключить статус переоткрытия")
def change_reopen(modeladmin, request, queryset):
    updated_count = 0
    for task in queryset:
        task.is_reopened = not task.is_reopened
        task.save()
        updated_count += 1

    modeladmin.message_user(
        request,
        f"Статус переоткрытия изменён для {updated_count} задач."
    )

@admin.action(description="Отметить задачи как завершенные")
def status_to_completed(modeladmin, request, queryset):
    queryset.update(status='COMPLETED')
    modeladmin.message_user(
        request,
        f"Статус выбранных вами задач изменен на 'COMPLETED' "
    )
@admin.action(description="Отметить задачи как отмененные")
def status_to_canceled(modeladmin, request, queryset):
    queryset.update(status='CANCELED')
    modeladmin.message_user(
        request,
        f"Статус выбранных вами задач изменен на 'CANCELED' "
    )

@admin.action(description="Processed by admin")
def admin_processed(modeladmin, request, queryset):
    comments_to_create = []

    for task in queryset:
        comments_to_create.append(
            Comments(
                task=task,
                message="Processed by admin",
                user=request.user,
            )
        )

    created_count = Comments.objects.bulk_create(comments_to_create)
    modeladmin.message_user(
        request,
        f"Добавлен комментарий Processed by admin к выбранным вами задачам"
    )

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
    # exclude = ('is_reopened',)
    list_display = (
        "display_name",
        "status",
        "priority",
        "project",
        "assignee",
        "priority_status",
        'is_reopened'
    )
    list_display_links = ("display_name",)
    # list_display_links = ("name", "status")
    list_editable = ("status", "priority")
    readonly_fields = ("created_at",)
    list_filter = ("status","priority","project")
    inlines = (CommentInline, TagInline )
    actions = [
        change_reopen,
        status_to_canceled,
        status_to_completed,
        admin_processed,
    ]
    def priority_status(self, obj):
        if obj.priority < 3:
            color = "#28a745"
            text = "LOW"
        elif obj.priority < 5:
            color = "#ffc107"
            text = "MEDIUM"
        else:
            color = "#dc3545"
            text = "HIGH"

        return mark_safe(
            f'<span style="color: {color};'f' font-weight: bold;">{text}</span>'
        )
    priority_status.string = ""
    priority_status.short_description = "Приоритет статуса"

    @admin.display(description='Наименование')
    def display_name(self, instance):
        return mark_safe(f"<h1>{instance.name}</h1>")





class ProjectsAdmin(admin.ModelAdmin):
    # fields = ('name', 'description')
    exclude = ('owner',)
    inlines = (ProjectDetailsInLine,)
    # list_display = ("name", "status", "priority", "project", "assignee")
    # list_display_links = ("name")
    # # list_display_links = ("name", "status")
    # list_editable = ("status", "priority")
    # readonly_fields = ("created_at",)

class AttachmentsAdmin(admin.ModelAdmin):
    list_display = ("name", "task", "display_photo", "photo")
    @admin.display(description="Превью")
    def display_photo(self, instance):
        if instance.photo:
            return mark_safe(f"<img src='{instance.photo.url}' width='15%' />")




admin.site.register(Tags)
admin.site.register(Tasks, TasksAdmin)
admin.site.register(Comments)
admin.site.register(ProjectDetails)
admin.site.register(Projects, ProjectsAdmin)
admin.site.register(Attachments, AttachmentsAdmin)






