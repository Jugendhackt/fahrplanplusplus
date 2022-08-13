from datetime import datetime
from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action

from .serializers import EventSerializer, VenueSerializer, PerformanceSerializerPlain
from .models import Event, Venue, Performance
from .upstream import update as upstream_update
import channels.layers
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from django.forms.models import model_to_dict
import json
from django.core.serializers.json import DjangoJSONEncoder

def broadcast_status():
	
	async_to_sync(get_channel_layer().group_send)(
        "dashboard",
		{"type":"dashboard_message","data":json.dumps(build_dict(), cls=DjangoJSONEncoder)}
    )

def build_dict():
	data = {
		"venues": {},
		"time": datetime.now()
	}
	for v in Venue.objects.all():
		serializer = PerformanceSerializerPlain(Performance.objects.filter(venue=v.id).order_by("planned_start"),many=True)
		data["venues"][str(v.id)] = {"venue":model_to_dict(v)}
		data["venues"][str(v.id)] = {"talks": serializer.data}
	

	return data