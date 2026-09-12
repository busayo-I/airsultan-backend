from django.urls import path
from .views import LoginView, LogoutView, ChangePasswordView, MeView

urlpatterns = [
    path('login/',           LoginView.as_view(),          name='admin-login'),
    path('logout/',          LogoutView.as_view(),          name='admin-logout'),
    path('change-password/', ChangePasswordView.as_view(),  name='admin-change-password'),
    path('me/',              MeView.as_view(),              name='admin-me'),
]