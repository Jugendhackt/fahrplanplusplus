from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import EventSerializer, VenueSerializer
from .models import Event, Venue

class EventViewSet(viewsets.ModelViewSet):
	"""
	Show/Edit Events
	"""
	queryset = Event.objects.all()
	serializer_class = EventSerializer
	permission_classes = [permissions.AllowAny]

class VenueViewSet(viewsets.ModelViewSet):
	"""
	Show/Edit Events
	"""
	queryset = Venue.objects.all()
	serializer_class = VenueSerializer
	permission_classes = [permissions.AllowAny]