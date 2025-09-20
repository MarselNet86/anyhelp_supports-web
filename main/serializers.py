from rest_framework import serializers
from .models import Support, FieldSupport


class SupportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Support
        fields = (
            "id",
            "settlement", "branch", "support_number", "name",
            "address", "longitude", "latitude",
            "commissioning_date", "owner", "material",
        )
        
        
class FieldSupportSerializer(serializers.ModelSerializer):
    created_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model  = FieldSupport
        fields = [
            "id",
            "photo", "comment", "status", "address",
            "latitude", "longitude",
            "created_by", "created_at", "updated_at",
        ]
        read_only_fields = ["created_by", "created_at", "updated_at"]