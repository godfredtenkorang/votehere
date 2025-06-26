from django import forms
from .models import EventOrganizer

class EventOrganizerForm(forms.ModelForm):
    class Meta:
        model = EventOrganizer
        fields = [
            'event_name', 
            'organization_name', 
            'contact_name', 
            'phone_number', 
            'email', 
            'event_description', 
            'event_type', 
            'promo_code'
        ]
        widgets = {
            'event_description': forms.Textarea(attrs={'rows': 4}),
            'event_type': forms.RadioSelect()
        }