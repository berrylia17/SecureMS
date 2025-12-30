from django.urls import path
from django.contrib.auth import views as auth_views
from .views import register_view, edit_profile_view, logout_view, change_password_view

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(
        template_name='accounts/login.html'
    ), name='login'),

    path('logout/', logout_view, name='logout'),

    path('register/', register_view, name='register'),

    path('edit-profile/', edit_profile_view, name='edit_profile'),

    path('change-password/', change_password_view, name='change_password'),
]
