import json
from datetime import datetime

import channels.layers
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.core.serializers.json import DjangoJSONEncoder
from django.forms.models import model_to_dict
from rest_framework import permissions, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, Performance, Venue
from .serializers import (EventSerializer, PerformanceSerializerPlain,
                          VenueSerializer)
from .upstream import update as upstream_update


def broadcast_status():
	
	async_to_sync(get_channel_layer().group_send)(
        "dashboard",
		{"type":"dashboard_message","data":json.dumps(build_dict(), cls=DjangoJSONEncoder)}
    )

def build_dict():
	data = {
		"venues": {},
		"global_time": datetime.now()
	}
	for v in Venue.objects.all():
		performances = Performance.objects.filter(venue=v.id).order_by("planned_start")
		serializer = PerformanceSerializerPlain(performances,many=True)
		# we have another time per event, calculated by the event model.
		data["venues"][str(v.id)] = {"venue":model_to_dict(v), "talks": serializer.data, "time": v.event.current_time}

	return data