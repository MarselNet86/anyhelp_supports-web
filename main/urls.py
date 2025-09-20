from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('', views.supports_upload_view, name='supports_upload'),
    path("supports_export/", views.supports_export_view, name="supports_export"),

    # принять (accepted) или отклонить (rejected с комментом)
    path("supports/<int:pk>/update-status/", views.update_support_status, name="update_support_status"),

    # экспорт zip (выбранные POST ids[] — при необходимости автоматически принимаем)
    path("supports/export-photos/", views.export_support_photos, name="export_support_photos"),
    ]
