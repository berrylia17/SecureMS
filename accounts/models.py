from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class EmailOTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    code = models.CharField(max_length=6, blank=True, null=True)
    created_at = models.DateTimeField(auto_now=True)

    def generate_code(self):
        import random
        self.code = str(random.randint(100000, 999999))
        self.created_at = timezone.now()
        self.save()
        return self.code

    def is_valid(self):
        return timezone.now() < self.created_at + timedelta(minutes=5)

