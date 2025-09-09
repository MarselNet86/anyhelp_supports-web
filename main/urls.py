from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path('', views.supports_upload_view, name='supports_upload'),
    path('supports/upload/progress/', views.upload_progress, name='upload_progress'),
]
