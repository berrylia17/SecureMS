# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
import unicodedata
import logging

logger = logging.getLogger('accounts')


def normalize_input(value: str) -> str:
    """Normalize Unicode input to NFC form to prevent homoglyph attacks."""
    if value is None:
        return value
    return unicodedata.normalize("NFC", value)


# Safe regex validator for usernames
username_validator = RegexValidator(
    regex=r"^[a-zA-Z0-9_]{3,20}$",
    message="Username must be 3–20 characters, letters/numbers/underscores only."
)


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=150, validators=[username_validator])

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        normalized = normalize_input(username)
        # Log invalid attempts
        if normalized and not username_validator.regex.match(normalized):
            logger.warning(f"Invalid username attempt: {normalized}")
        return normalized

    def clean_email(self):
        email = self.cleaned_data.get("email")
        normalized = normalize_input(email)
        try:
            forms.EmailField().clean(normalized)
        except forms.ValidationError:
            logger.warning(f"Invalid email attempt: {normalized}")
        return normalized


class ProfileUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=150, validators=[username_validator])

    class Meta:
        model = User
        fields = ["username", "email", "first_name", "last_name"]

    def clean_username(self):
        username = self.cleaned_data.get("username")
        normalized = normalize_input(username)
        if normalized and not username_validator.regex.match(normalized):
            logger.warning(f"Invalid username attempt: {normalized}")
        return normalized

    def clean_email(self):
        email = self.cleaned_data.get("email")
        normalized = normalize_input(email)
        try:
            forms.EmailField().clean(normalized)
        except forms.ValidationError:
            logger.warning(f"Invalid email attempt: {normalized}")
        return normalized
