from django.contrib import admin
from django.urls import path, include
from core import views as core_views

urlpatterns = [
    path('', core_views.home, name='home'),          # Home page
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('booking/', include('booking.urls')),
]


# Custom error handlers (templates provided in templates/errors/ or templates/500.html)
handler400 = 'django.views.defaults.bad_request'
handler403 = 'django.views.defaults.permission_denied'
handler404 = 'django.views.defaults.page_not_found'
handler500 = 'django.views.defaults.server_error'
