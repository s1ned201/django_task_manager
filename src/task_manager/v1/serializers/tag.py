from rest_framework import serializers

from task_manager.models import Tags


class TagSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Tags
        fields = (
            'id',
            'name',
        )
