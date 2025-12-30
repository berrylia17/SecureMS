from django.contrib import admin
from .models import Booking

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'booth_type', 'date', 'created_at')
    list_filter = ('date',)
    search_fields = ('user__username', 'booth_type')
