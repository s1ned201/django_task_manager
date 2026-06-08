from rest_framework import serializers
import django_filters
from account.models import User
from task_manager.models import Tasks, Projects
from task_manager.v1.serializers.comment import CommentsSerializer
from task_manager.v1.serializers.tag import TagSerializer
from task_manager.v1.serializers.project import ProjectSerializer

class TaskQueryFilterSerializer(django_filters.FilterSet):
    name = django_filters.CharFilter(lookup_expr='iexact')
    # priority__gt = django_filters.NumberFilter(field_name='priority', lookup_expr='gt')
    # priority__lt = django_filters.NumberFilter(field_name='priority', lookup_expr='lt')
    created_at__gte = django_filters.NumberFilter(field_name='created_at', lookup_expr='gte')
    created_at__lte = django_filters.NumberFilter(field_name='created_at', lookup_expr='lte')
    ordering = django_filters.OrderingFilter(
        fields=(
        ('priority', 'priority'),
        ('created_at', 'created_at')
        )
    )
    class Meta:
        model = Tasks
        fields = ('name', 'priority', 'status', 'created_at')


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


