from django import forms
from django.core.exceptions import ValidationError
from .models import SecurityEvent


class SecurityEventForm(forms.ModelForm):
    class Meta:
        model = SecurityEvent
        fields = ['category', 'timestamp', 'severity', 'source', 'threat_score']
        widgets = {
            'timestamp': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def clean_threat_score(self):
        threat_score = self.cleaned_data.get('threat_score')
        if threat_score is not None and threat_score <= 0:
            raise ValidationError('Threat score must be greater than 0.')
        return threat_score
