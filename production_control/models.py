from django.db import models

# example json: https://pretalx.margau.net/dtjhhnfm2022/schedule/export/schedule.json

class Event(models.Model):
	name = models.CharField(max_length=200)
	upstream_agenda_url = models.URLField(blank=True)
	upstream_name = models.CharField(max_length=200, blank=True)

class Venue(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	upstream_name = models.CharField(max_length=200, blank=True)

class Performance(models.Model):
	# in general it is possible that no performance at all is running
	class StartCondition(models.IntegerChoices):
		MANUAL = 0
		AUTO_TIME = 1
		AUTO_PREVIOUS = 2
	# additionally, implicit stop is done by start of the next
	class EndCondition(models.IntegerChoices):
		MANUAL = 0
		AUTO_DURATION = 1
	
	venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	upstream_uuid = models.UUIDField(blank=True)
	planned_start = models.DateTimeField()
	actual_start = models.DateTimeField(blank=True)
	planned_duration = models.IntegerField()
	actual_duration = models.IntegerField(blank=True)
	start = models.IntegerField(choices=StartCondition.choices, default=0)
	end = models.IntegerField(choices=EndCondition.choices, default=0)
