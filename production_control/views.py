from rest_framework import viewsets, permissions, status
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
		serializer = PerformanceSerializer(Performance.objects.filter(venue=self.get_object().id).order_by("planned_start"),many=True,context={'request': request})
		return Response(serializer.data)

class PerformanceViewSet(viewsets.ModelViewSet):
	"""
	Show/Edit Events
	"""
	queryset = Performance.objects.all()
	serializer_class = PerformanceSerializer
	permission_classes = [permissions.AllowAny]
	
	@action(detail=True,methods=["POST"])
	def start(self, request, pk):
		perf = self.get_object()
		if perf.actual_start:
			return Response("Performance Already started", status.HTTP_400_BAD_REQUEST)
		perf.actual_start = perf.venue.event.current_time
		perf.save()
		return Response(PerformanceSerializer(perf,context={'request': request}).data)
