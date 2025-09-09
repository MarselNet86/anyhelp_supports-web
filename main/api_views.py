from rest_framework import viewsets, permissions
from django_filters.rest_framework import FilterSet, filters
from .models import Support
from .serializers import SupportSerializer

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
