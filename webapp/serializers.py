# webapp/serializers.py

from rest_framework import serializers

class ActionItemSerializer(serializers.Serializer):
    """Serializer for a single action item."""
    description = serializers.CharField()
    assignee = serializers.CharField(allow_null=True)
    due_date = serializers.CharField(allow_null=True)
    is_completed = serializers.BooleanField()

class MeetingSerializer(serializers.Serializer):
    """Serializer for a full meeting with its action items."""
    id = serializers.CharField(source='_id')
    meeting_title = serializers.CharField()
    created_at = serializers.DateTimeField()
    total_actions = serializers.IntegerField()
    action_items = ActionItemSerializer(many=True)