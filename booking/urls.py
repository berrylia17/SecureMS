from django.urls import path
from . import views

urlpatterns = [
    path('', views.BookingListView.as_view(), name='booking_list'),
    path('create/', views.BookingCreateView.as_view(), name='booking_create'),
    path('<int:pk>/edit/', views.BookingUpdateView.as_view(), name='booking_edit'),
    path('<int:pk>/delete/', views.BookingDeleteView.as_view(), name='booking_delete'),
]
