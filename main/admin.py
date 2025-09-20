from django.contrib import admin
from .models import Support, FieldSupport


@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    list_display = ("id", "settlement", "branch", "support_number", "status")
    list_filter = ("status", "settlement", "branch")
    search_fields = ("support_number", "name", "address", "owner")


@admin.register(FieldSupport)
class FieldSupportAdmin(admin.ModelAdmin):
    list_display  = ("id", "status", "created_by", "created_at")
    list_filter   = ("status", "created_at")
    search_fields = ("comment", "address")