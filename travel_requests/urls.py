from django.urls import path
from .views import (
    TravelRequestListView,
    TravelRequestDetailView,
    TravelRequestCreateView,
)

urlpatterns = [
    # Admin endpoints (protected)
    path('',         TravelRequestListView.as_view(),   name='travel-request-list'),
    path('<int:pk>/', TravelRequestDetailView.as_view(), name='travel-request-detail'),

    # Public endpoint (no auth needed)
    path('submit/',  TravelRequestCreateView.as_view(), name='travel-request-submit'),
]