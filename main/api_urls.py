from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api_views import SupportViewSet

router = DefaultRouter()
router.register(r"supports", SupportViewSet, basename="support")

urlpatterns = [
    path("", include(router.urls)),
]