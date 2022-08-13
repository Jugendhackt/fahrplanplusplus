from django.db import models
import uuid
import datetime

# example json: https://pretalx.margau.net/dtjhhnfm2022/schedule/export/schedule.json

class Event(models.Model):
	def __str__(self):
		return 'Event: ' + self.name

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	name = models.CharField(max_length=200)
	upstream_agenda_url = models.URLField(blank=True)
	upstream_name = models.CharField(max_length=200, blank=True)

class Venue(models.Model):
	def __str__(self):
		return 'Venue: ' + self.name

	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	upstream_name = models.CharField(max_length=200, blank=True)

class Performance(models.Model):
	def __str__(self):
		return 'Performance: ' + self.name

	# in general it is possible that no performance at all is running
	class StartCondition(models.IntegerChoices):
		MANUAL = 0
		AUTO_TIME = 1
		AUTO_PREVIOUS = 2
	# additionally, implicit stop is done by start of the next
	class EndCondition(models.IntegerChoices):
		MANUAL = 0
		AUTO_DURATION = 1
	
	id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
	venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
	name = models.CharField(max_length=200)
	upstream_uuid = models.UUIDField(blank=True)
	planned_start = models.DateTimeField()
	actual_start = models.DateTimeField(blank=True, null=True)
	planned_duration = models.IntegerField()
	actual_duration = models.IntegerField(blank=True, null=True)
	start = models.IntegerField(choices=StartCondition.choices, default=0)
	end = models.IntegerField(choices=EndCondition.choices, default=0)

	@property
	def planned_end(self):
		end = self.planned_start + datetime.timedelta(0, self.planned_duration)
		return end
	
	@property
	def actual_end(self):
		end = 0
		if self.actual_start and self.actual_duration:
			end = self.actual_start + datetime.timedelta(0, self.actual_duration)
			print(end)
		return end

	@property
	def delay_seconds(self):
		delay_seconds = 0
		i = 0
		all_performances = Performance.objects.filter(venue=self.venue).order_by("planned_start")
		# loop over all performances to find delay
		while i < len(all_performances):
			p = all_performances[i]
						
			# default case: no actual data available
			# first case: we are running, have no actual end yet, so the delay 
			if p.actual_start:
				delay_seconds = (p.actual_start-p.planned_start).total_seconds()
			# if we are already done, set the end delay
			if p.actual_end:
				delay_seconds = (p.actual_end-p.planned_end).total_seconds()
			
			# if we are not the first check
			if i > 0 and all_performances[i-1]:
				# if our start is later or equal than the previous estimated end, no delay is left
				if p.planned_start >= all_performances[i-1].estimated_end:
					delay_seconds = 0
				# otherwise, the delay is the time delay between the prev. end and our planned start
				else:
					delay_seconds = (all_performances[i-1].estimated_end - p.planned_start).total_seconds()

			# if this is our searched performance, stop here
			if p.id == self.id:
				return delay_seconds
			
			i+=1

		print(delay_seconds)
		return delay_seconds

	@property
	def estimated_start(self):
		ret = 0
		# if we already have an actual start, that is our estimated start
		if self.actual_start:
			ret = self.actual_start
		else:
			ret = self.planned_start + datetime.timedelta(0, self.delay_seconds)
		return ret
	
	@property
	def estimated_end(self):
		if self.actual_end:
			return self.actual_end
		return self.planned_end + datetime.timedelta(0, self.delay_seconds)