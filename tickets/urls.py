from django.urls import path
from .views import RegisterView, AdminScanView, AdminListView, MyTicketsView, HealthCheckView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('scan/', AdminScanView.as_view()),
    path('list/', AdminListView.as_view()),
    path('my-tickets/', MyTicketsView.as_view()),
    path('health/', HealthCheckView.as_view(), name='health-check'),
]