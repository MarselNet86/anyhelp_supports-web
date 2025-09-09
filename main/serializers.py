from rest_framework import serializers
from .models import Support


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = (
            "id",
            "settlement", "branch", "support_number", "name",
            "address", "longitude", "latitude",
            "commissioning_date", "owner", "material",
        )