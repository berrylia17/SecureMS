from django.contrib.auth.mixins import UserPassesTestMixin

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        # allow superusers
        if user.is_superuser:
            return True
        return user.groups.filter(name='Admin').exists()
