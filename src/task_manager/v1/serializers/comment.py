from rest_framework import serializers
from task_manager.models.comments import Comments

class CommentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comments
        fields = ('id', 'message')
