from rest_framework import serializers

from account.models import User
from task_manager.models import Tasks, Projects
from task_manager.v1.serializers.comment import CommentsSerializer
from task_manager.v1.serializers.tag import TagSerializer
from task_manager.v1.serializers.project import ProjectSerializer


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    is_reopened = serializers.BooleanField(read_only=True)
    project = ProjectSerializer(read_only=True)
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    comments = CommentsSerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)

    class Meta:
        model = Tasks
        fields = (
            'id',
            'name',
            'description',
            'priority',
            'status',
            'is_reopened',
            'project',
            'assignee',
            'comments',
            'tags',
        )

