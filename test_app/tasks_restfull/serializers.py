from rest_framework import serializers
from tasks.models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
                'id', 'title', 'descriptions', 'completed',
                'created_at', 'updated_at', 'user'
        ]
        read_only_fields = ['created_at', 'updated_at']


    def validate_title(self, value):
        if len(value) < 3:
            raise serializers.ValidationError("Title must be at least 3 characters long.")
        return value
