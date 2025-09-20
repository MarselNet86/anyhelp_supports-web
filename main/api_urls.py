from rest_framework.routers import DefaultRouter
from django.urls import path, include
from .api_views import SupportViewSet, FieldSupportViewSet

router = DefaultRouter()
router.register(r"supports", SupportViewSet, basename="support")
router.register(r"field-supports", FieldSupportViewSet, basename="field-support")

urlpatterns = [
    path("", include(router.urls)),
]