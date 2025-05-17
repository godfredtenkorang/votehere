from django import forms

from vote.models import Category
from .models import SendSms
from payment.models import Nominees
from ussd.models import PaymentTransaction


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
        
class CategorySMSForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    message = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'rows': 4,
            'placeholder': 'Enter your SMS message here...'
        }),
        label="SMS Message",
        max_length=350  # Standard SMS length
    )
    
class PaymentTransactionForm(forms.ModelForm):
    class Meta:
        model = PaymentTransaction
        fields = ['invoice_no', 'amount', 'nominee_code', 'votes', 'category']