from rest_framework import serializers

from task_manager.models import Attachments


class AttachmentSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)
    file = serializers.FileField(read_only=True)

    class Meta:
        model = Attachments
        fields = (
            'id',
            'name',
            'file',
        )
