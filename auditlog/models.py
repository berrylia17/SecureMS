from django.db import models
from django.conf import settings

class AuditEntry(models.Model):
    ACTION_CHOICES = [
        ('login_success', 'Login success'),
        ('login_failed', 'Login failed'),
        ('logout', 'Logout'),
        ('create', 'Create'),
        ('update', 'Update'),
        ('delete', 'Delete'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,
                             on_delete=models.SET_NULL, related_name='audit_entries')
    username = models.CharField(max_length=150, blank=True)
    action = models.CharField(max_length=32, choices=ACTION_CHOICES, default='other')
    path = models.CharField(max_length=500, blank=True)
    method = models.CharField(max_length=10, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    message = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        return (self.user.username if self.user else self.username) + " - " + self.action
