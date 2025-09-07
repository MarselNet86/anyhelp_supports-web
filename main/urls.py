from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('login/', views.login_view, name='login'),
    path('logout/', views.login_view, name='logout'),
    path('', views.home_view, name='home'),
]
