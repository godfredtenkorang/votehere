from django import forms

from vote.models import Category, SubCategory
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
        fields = '__all__'
        
        widgets = {
            'date_added': forms.DateTimeInput(attrs={'type': 'date'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'date'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set the subcategory queryset based on the selected category
        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['sub_category'].queryset = SubCategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk and self.instance.category:
            self.fields['sub_category'].queryset = self.instance.category.subcategory_set.all()
        else:
            self.fields['sub_category'].queryset = SubCategory.objects.none()
        
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
        

class AccessCodeSMSForm(forms.Form):
    name = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter name'
        }),
        label='SMS Name',
    )
    phone_number = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter phone number'
        }),
        label='SMS Phone Number',
    )
    access_code = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Access Code'
        }),
        label='SMS Access Code',
    )
    category = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Enter Category'
        }),
        label='SMS Category',
    )
