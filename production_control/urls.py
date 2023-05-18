from rest_framework import routers
from django.urls import path


from . import views

router = routers.DefaultRouter()
router.register(r"event", views.EventViewSet)
router.register(r"venue", views.VenueViewSet)
router.register(r"performance", views.PerformanceViewSet)

urlpatterns = router.urls
# TODO: provide directly filtered event lists
# urlpatterns.append(path('event/<uuid:event_id>/performance/', views.PerformanceViewSet.as_view({'get': 'list'})))
# urlpatterns.append(path('event/<uuid:event_id>/performance/<uuid:performance_id>/', views.PerformanceViewSet.as_view({'get': 'retrieve'})))

