from rest_framework import serializers
from task_manager.models import Projects


class ProjectSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)
    owner = serializers.PrimaryKeyRelatedField(read_only=True)
    owner_name = serializers.CharField(source='owner.email', read_only=True)

    class Meta:
        model = Projects
        fields = (
            'id',
            'name',
            'description',
            'owner',
            'owner_name',
        )
