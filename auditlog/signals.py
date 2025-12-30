from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed
from django.dispatch import receiver
from .models import AuditEntry

def get_ip(request):
    if not request:
        return None
    xff = request.META.get("HTTP_X_FORWARDED_FOR")
    if xff:
        return xff.split(",")[0]
    return request.META.get("REMOTE_ADDR")

@receiver(user_logged_in)
def log_login_success(sender, request, user, **kwargs):
    AuditEntry.objects.create(
        user=user,
        username=user.username,
        action="login_success",
        path=request.path,
        method=request.method,
        ip_address=get_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", ""),
        message="User logged in"
    )

@receiver(user_logged_out)
def log_logout(sender, request, user, **kwargs):
    AuditEntry.objects.create(
        user=user,
        username=(user.username if user else ""),
        action="logout",
        path=request.path if request else "",
        method=request.method if request else "",
        ip_address=get_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", "") if request else "",
        message="User logged out"
    )

@receiver(user_login_failed)
def log_login_failed(sender, credentials, request, **kwargs):
    AuditEntry.objects.create(
        user=None,
        username=credentials.get("username", ""),
        action="login_failed",
        path=request.path if request else "",
        method=request.method if request else "",
        ip_address=get_ip(request),
        user_agent=request.META.get("HTTP_USER_AGENT", "") if request else "",
        message="Failed login attempt"
    )
