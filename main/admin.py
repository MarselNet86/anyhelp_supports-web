from django.contrib import admin
from .models import Support

@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
    # таблица списка
    list_display = (
        "id", "settlement", "branch", "support_number", "name",
        "owner", "material", "commissioning_date", "has_coords",
    )
    list_display_links = ("id", "support_number", "name")
    list_per_page = 50
    ordering = ("settlement", "support_number")

    # фильтры и поиск
    list_filter = ("settlement", "branch", "owner", "material")
    search_fields = (
        "support_number", "name", "address",
        "settlement", "branch", "owner",
    )
    date_hierarchy = "commissioning_date"

    # форма редактирования
    fieldsets = (
        ("Идентификация", {
            "fields": ("settlement", "branch", "support_number", "name"),
        }),
        ("Расположение", {
            "fields": ("address", ("longitude", "latitude")),
        }),
        ("Эксплуатация", {
            "fields": ("commissioning_date", "owner", "material"),
        }),
        ("Служебное", {
            "fields": ("has_coords",),
            "classes": ("collapse",),
        }),
    )
    readonly_fields = ("has_coords",)

    # небольшая «подсказка» в форме координат
    help_texts = {
        "longitude": "Напр.: 73.2554337414",
        "latitude": "Напр.: 61.2647237504",
    }

    # вычисляемое поле в списке/форме
    def has_coords(self, obj):
        return bool(obj.longitude and obj.latitude)
    has_coords.short_description = "Координаты заданы"
    has_coords.boolean = True

    # массовые действия
    actions = ["clear_coords"]

    def clear_coords(self, request, queryset):
        updated = queryset.update(longitude=None, latitude=None)
        self.message_user(request, f"Очищены координаты у {updated} объектов.")
    clear_coords.short_description = "Очистить координаты у выбранных"