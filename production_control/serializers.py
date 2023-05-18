from rest_framework import serializers

from .models import Event, Performance, Venue, PerformanceAnnotation


class EventSerializer(serializers.HyperlinkedModelSerializer):
    current_time = serializers.ReadOnlyField()

    class Meta:
        model = Event
        fields = "__all__"


class VenueSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Venue
        fields = "__all__"

class PerformanceAnnotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PerformanceAnnotation
        fields = "__all__"

class PerformanceSerializer(serializers.HyperlinkedModelSerializer):
    planned_end = serializers.ReadOnlyField()
    actual_end = serializers.ReadOnlyField()
    estimated_start = serializers.ReadOnlyField()
    estimated_end = serializers.ReadOnlyField()
    delay_seconds = serializers.ReadOnlyField()
    annotations = PerformanceAnnotationSerializer(many=True, read_only=True, source='performanceannotation_set')

    class Meta:
        model = Performance
        fields = "__all__"
        extra_fields = ['annotations']

    def get_field_names(self, declared_fields, info):
        expanded_fields = super(PerformanceSerializer, self).get_field_names(declared_fields, info)

        if getattr(self.Meta, 'extra_fields', None):
            return expanded_fields + self.Meta.extra_fields
        else:
            return expanded_fields

class PerformanceSerializerPlain(serializers.ModelSerializer):
    planned_end = serializers.ReadOnlyField()
    actual_end = serializers.ReadOnlyField()
    estimated_start = serializers.ReadOnlyField()
    estimated_end = serializers.ReadOnlyField()
    delay_seconds = serializers.ReadOnlyField()

    class Meta:
        model = Performance
        fields = "__all__"
