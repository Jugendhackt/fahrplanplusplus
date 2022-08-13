from rest_framework import serializers

from .models import Event

#class UpstreamUpdateRequestSerializer(serializers.Serializer):
#   """Upstream Update Request"""
#   uuid = serializers.UUIDField()
#   upstream_url = serializers.URLField()

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'name', 'upstream_agenda_url', 'upstream_name']