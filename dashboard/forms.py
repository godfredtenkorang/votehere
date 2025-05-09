from django import forms
from .models import SendSms
from payment.models import Nominees


class SendSmsForm(forms.ModelForm):
    class Meta:
        model = SendSms
        fields = ['name', 'phone_number', 'category']
        

class NomineeForm(forms.ModelForm):
    class Meta:
        model = Nominees
        fields = ['category', 'sub_category', 'name', 'image', 'total_vote', 'code', 'date_added', 'end_date']
        
        widgets = {
            'date_added': forms.DateTimeInput(),
            'end_date': forms.DateTimeInput(),
        }