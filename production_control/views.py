from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import EventSerializer, VenueSerializer, PerformanceSerializer
from .models import Event, Venue, Performance
from .upstream import update as upstream_update
import channels.layers
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.forms.models import model_to_dict
import json
from django.core.serializers.json import DjangoJSONEncoder
from . import broadcast

class EventViewSet(viewsets.ModelViewSet):
	"""
	Show/Edit Events
	"""
	queryset = Event.objects.all()
	serializer_class = EventSerializer
	permission_classes = [permissions.AllowAny]
	
	@action(detail=True, methods=['post'])
	def update_upstream(self, request, pk):
		upstream_update(self.get_object())
		# todo: Error Handling
		return Response()

class VenueViewSet(viewsets.ModelViewSet):
	"""
	Show/Edit Venues
	"""
	queryset = Venue.objects.all()
	serializer_class = VenueSerializer
	permission_classes = [permissions.AllowAny]

	@action(detail=True)
	def current_timeline(self, request, pk):
		# todo: Error Handling
		broadcast.broadcast_status()
		serializer = PerformanceSerializer(Performance.objects.filter(venue=self.get_object().id).order_by("planned_start"),many=True,context={'request': request})
		return Response(serializer.data)

class PerformanceViewSet(viewsets.ModelViewSet):
	"""
	Show/Edit Events
	"""
	queryset = Performance.objects.all()
	serializer_class = PerformanceSerializer
	permission_classes = [permissions.AllowAny]
	