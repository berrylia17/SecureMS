from django.urls import path
from .views import (
    register_view,
    edit_profile_view,
    logout_view,
    change_password_view,
    login_view,
    mfa_verify_view,
)

urlpatterns = [
    # Custom login with MFA
    path('login/', login_view, name='login'),
    path('mfa-verify/', mfa_verify_view, name='mfa_verify'),

    # Logout
    path('logout/', logout_view, name='logout'),

    # Registration
    path('register/', register_view, name='register'),

    # Profile management
    path('edit-profile/', edit_profile_view, name='edit_profile'),

    # Password change
    path('change-password/', change_password_view, name='change_password'),
]
