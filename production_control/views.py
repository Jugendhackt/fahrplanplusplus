from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Event, Performance, Venue
from .serializers import EventSerializer, PerformanceSerializer, VenueSerializer
from .upstream import update as upstream_update


class EventViewSet(viewsets.ModelViewSet):
    """
    Show/Edit Events
    """

    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=["post"])
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
        serializer = PerformanceSerializer(
            Performance.objects.filter(venue=self.get_object().id).order_by(
                "planned_start"
            ),
            many=True,
            context={"request": request},
        )
        return Response(serializer.data)


class PerformanceViewSet(viewsets.ModelViewSet):
    """
    Show/Edit Events
    """

    queryset = Performance.objects.all()
    serializer_class = PerformanceSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=True, methods=["POST"])
    def start(self, request, pk):
        perf = self.get_object()
        if perf.actual_start:
            return Response("Performance Already started", status.HTTP_400_BAD_REQUEST)
        perf.actual_start = perf.venue.event.current_time
        perf.save()
        return Response(PerformanceSerializer(perf, context={"request": request}).data)

    @action(detail=True, methods=["POST"])
    def end(self, request, pk):
        perf = self.get_object()
        if perf.actual_end:
            return Response("Performance already ended", status.HTTP_400_BAD_REQUEST)
        if not perf.actual_start:
            return Response("Performance not started yet", status.HTTP_400_BAD_REQUEST)

        end = perf.venue.event.current_time
        perf.actual_duration = (end - perf.actual_start).seconds
        perf.save()
        return Response(PerformanceSerializer(perf, context={"request": request}).data)
