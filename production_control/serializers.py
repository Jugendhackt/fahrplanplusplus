from rest_framework import serializers

from .models import Event, Performance, Venue


class EventSerializer(serializers.HyperlinkedModelSerializer):
    current_time = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = "__all__"


class VenueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Venue
        fields = "__all__"


class PerformanceSerializer(serializers.HyperlinkedModelSerializer):
    planned_end = serializers.ReadOnlyField()
    actual_end = serializers.ReadOnlyField()
    estimated_start = serializers.ReadOnlyField()
    estimated_end = serializers.ReadOnlyField()
    delay_seconds = serializers.ReadOnlyField()

    class Meta:
        model = Performance
        fields = "__all__"


class PerformanceSerializerPlain(serializers.ModelSerializer):
    planned_end = serializers.ReadOnlyField()
    actual_end = serializers.ReadOnlyField()
    estimated_start = serializers.ReadOnlyField()
    estimated_end = serializers.ReadOnlyField()
    delay_seconds = serializers.ReadOnlyField()

    class Meta:
        model = Performance
        fields = "__all__"
