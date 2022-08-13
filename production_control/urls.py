from django.urls import path, include
from rest_framework import routers
from . import views

router = routers.DefaultRouter()
router.register(r'event',views.EventViewSet)
router.register(r'venue',views.VenueViewSet)
router.register(r'performance',views.PerformanceViewSet)

urlpatterns = router.urls