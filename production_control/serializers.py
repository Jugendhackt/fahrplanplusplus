from rest_framework import serializers

from .models import Event, Performance, Venue

class EventSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Event
		fields = '__all__'

class VenueSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Venue
		fields = '__all__'

class PerformanceSerializer(serializers.HyperlinkedModelSerializer):
	class Meta:
		model = Performance
		fields = '__all__'
