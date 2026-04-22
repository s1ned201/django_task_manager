from rest_framework import serializers

from account.models import User
from task_manager.models import Tasks, Projects
from task_manager.v1.serializers.comment import CommentsSerializer


class TaskSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    status = serializers.CharField(read_only=True)
    is_reopened = serializers.BooleanField(read_only=True)
    project = serializers.PrimaryKeyRelatedField(queryset=Projects.objects.all())
    assignee = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    comments = CommentsSerializer(many=True, read_only=True)

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
        )

