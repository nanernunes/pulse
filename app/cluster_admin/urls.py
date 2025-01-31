from django.urls import path
from . import views

urlpatterns = [
    path("", views.connect_to_elasticsearch, name="connect"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path('api/dashboard', views.get_dashboard_data, name='get_dashboard_data'),
]