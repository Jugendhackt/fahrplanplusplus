import json
import urllib.request

from dateutil import parser
from pytimeparse.timeparse import timeparse

from .models import Performance, Venue


def update(event):
	with urllib.request.urlopen(event.upstream_agenda_url) as url:
		data = json.loads(url.read().decode())
		schedule = data["schedule"]
		conference = schedule["conference"]
		# first update: upstream name
		event.upstream_name = conference["title"]
		event.save()
		# second: check room
		for room in conference["rooms"]:
			v, created = Venue.objects.get_or_create(
				event=event,
				upstream_name=room["name"]
			)
			# third: if the room is new, copy the room from upstream
			if created:
				v.name = room["name"]
			v.save()
		# now talks
		for day in conference["days"]:
			for roomname, room in day["rooms"].items():
				# match roomname with venue from db
				venue = Venue.objects.get(upstream_name = roomname)
				for upstream_perf in room:
					p_start = parser.parse(upstream_perf["start"])
					p_duration = timeparse(upstream_perf["duration"])*60
					p, created = Performance.objects.update_or_create(
						upstream_uuid = upstream_perf["guid"],
						defaults={
							"venue": venue,
							"planned_start": p_start,
							"planned_duration": p_duration,
							"name": upstream_perf["title"],
						},
					)