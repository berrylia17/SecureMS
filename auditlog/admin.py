from django.contrib import admin
from .models import AuditEntry

@admin.register(AuditEntry)
class AuditEntryAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_at', 'username', 'user', 'action', 'ip_address', 'path')
    list_filter = ('action', 'created_at')
    search_fields = ('username', 'user__username', 'ip_address', 'path', 'message')
    readonly_fields = [field.name for field in AuditEntry._meta.fields]

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
