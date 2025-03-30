from django import forms
from .models import SendSms


class SendSmsForm(forms.ModelForm):
    class Meta:
        model = SendSms
        fields = ['name', 'phone_number', 'category']