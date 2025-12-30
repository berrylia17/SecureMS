from django import forms
from .models import Booking
from django.core.exceptions import ValidationError
import re

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['booth_type', 'date', 'notes']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'notes': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_booth_type(self):
        v = self.cleaned_data.get('booth_type', '').strip()
        if not v:
            raise ValidationError("Booth type is required.")
        # whitelist: only letters, numbers, spaces, hyphen and ampersand
        if not re.match(r'^[\w\s\-\&]+$', v):
            raise ValidationError("Invalid characters in booth type.")
        return v
