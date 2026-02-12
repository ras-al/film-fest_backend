from django.urls import path
from .views import RegisterView, AdminScanView, AdminListView, MyTicketsView

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('scan/', AdminScanView.as_view()),
    path('list/', AdminListView.as_view()),
    path('my-tickets/', MyTicketsView.as_view()),
]