from rest_framework import viewsets, permissions
from django_filters.rest_framework import FilterSet, filters
from django.db import models
from .models import Support, FieldSupport
from .serializers import SupportSerializer, FieldSupportSerializer

class SupportFilter(FilterSet):
    settlement = filters.CharFilter(field_name="settlement", lookup_expr="icontains")
    branch = filters.CharFilter(field_name="branch", lookup_expr="icontains")
    support_number = filters.CharFilter(field_name="support_number", lookup_expr="icontains")

    class Meta:
        model = Support
        fields = ["settlement", "branch", "support_number", "owner", "material"]

class SupportViewSet(viewsets.ReadOnlyModelViewSet):
    """
    GET /api/supports/          — список (с пагинацией и фильтрами)
    GET /api/supports/{id}/     — детально
    """
    queryset = Support.objects.all().order_by("settlement", "support_number")
    serializer_class = SupportSerializer
    permission_classes = [permissions.IsAuthenticated]
    filterset_class = SupportFilter
    search_fields = ["name", "address", "settlement", "branch", "owner", "support_number"]
    ordering_fields = ["settlement", "branch", "support_number", "commissioning_date"]



class FieldSupportFilter(FilterSet):
    status   = filters.CharFilter(field_name="status", lookup_expr="exact")
    min_lat  = filters.NumberFilter(field_name="latitude",  lookup_expr="gte")
    max_lat  = filters.NumberFilter(field_name="latitude",  lookup_expr="lte")
    min_lon  = filters.NumberFilter(field_name="longitude", lookup_expr="gte")
    max_lon  = filters.NumberFilter(field_name="longitude", lookup_expr="lte")
    q        = filters.CharFilter(method="filter_q")

    def filter_q(self, queryset, name, value):
        # простой поиск по адресу и комментарию
        return queryset.filter(models.Q(address__icontains=value) | models.Q(comment__icontains=value))

    class Meta:
        model  = FieldSupport
        fields = ["status", "min_lat", "max_lat", "min_lon", "max_lon"]

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return getattr(obj, "created_by_id", None) == getattr(request.user, "id", None)

class FieldSupportViewSet(viewsets.ModelViewSet):
    """
    CRUD для полевых опор (независимы от инвентарных Support).
    Обычный пользователь видит/меняет только свои записи, is_staff — все.
    """
    serializer_class   = FieldSupportSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwnerOrReadOnly]
    filterset_class    = FieldSupportFilter
    search_fields      = ["address", "comment"]
    ordering_fields    = ["created_at", "status"]

    def get_queryset(self):
        qs = FieldSupport.objects.select_related("created_by").all()
        if not self.request.user.is_staff:
            qs = qs.filter(created_by=self.request.user)
        return qs.order_by("-created_at")

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)