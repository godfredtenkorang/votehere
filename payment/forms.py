from django import forms
from .models import Nominees

class NomineeForm(forms.ModelForm):
    class Meta:
        model = Nominees
        fields = ['category', 'sub_category', 'name', 'image', 'slug', 'code', 'date_added', 'end_date']
        widgets = {
            'date_added': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }