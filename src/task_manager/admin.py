from django.contrib import admin
from account.models import User
from task_manager.models import Tasks, Comments, ProjectDetails, Tags, Projects, Attachments

# Register your models here.

admin.site.register(User)
admin.site.register(Tags)
admin.site.register(Tasks)
admin.site.register(Comments)
admin.site.register(ProjectDetails)
admin.site.register(Projects)
admin.site.register(Attachments)






