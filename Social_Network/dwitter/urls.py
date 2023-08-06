from django.urls import path
from .views import dashboard, profile_list, profile, ProfileUpdateView

app_name = "dwitter"

urlpatterns = [
    path("dashboard", dashboard, name='dashboard'),
    path("accounts/profile", profile_list, name='profile_list'),
    path("profile/<int:pk>", profile, name='profile'),
    path("edit/", ProfileUpdateView.as_view(), name='edit'),
]