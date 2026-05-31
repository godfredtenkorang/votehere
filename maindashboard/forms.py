from django import forms

from payment.models import Nominees
from vote.models import Blog, SubCategory
from django.utils import timezone

class NomineeForm(forms.ModelForm):
    class Meta:
        model = Nominees
        fields = '__all__'
        
        widgets = {
            'date_added': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
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
        
        
class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'content', 'content1', 'content2', 'content3', 'content4', 'content5', 'image', 'blog_recommended', 'slug']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'content1': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'content2': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'content3': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'content4': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'content5': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'blog_recommended': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        
        
class NomineesForm(forms.ModelForm):
    class Meta:
        model = Nominees
        fields = ['category', 'sub_category', 'name', 'image', 'slug', 'total_vote', 'price_per_vote', 'can_vote', 'can_see_result', 'code', 'access_code', 'phone_number', 'date_added', 'end_date']
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'sub_category': forms.Select(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nominee name'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control', 'accept': 'image/*'}),
            'total_vote': forms.NumberInput(attrs={'class': 'form-control', 'value': '0'}),
            'price_per_vote': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'can_vote': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'can_see_result': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'access_code': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'date_added': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
        
        def clean_code(self):
            code = self.cleaned_data.get('code')
            if code and len(str(code)) != 4:
                raise forms.ValidationError("Code must be exactly 4 characters long.")
            return code
        
        def clean_access_code(self):
            access_code = self.cleaned_data.get('access_code')
            if access_code and len(str(access_code)) != 4:
                raise forms.ValidationError("Access code must be exactly 4 characters long.")
            return access_code
        
        def clean_end_date(self):
            end_date = self.cleaned_data.get('end_date')
            if end_date and end_date <= timezone.now():
                raise forms.ValidationError("End date must be in the future.")
            return end_date
        
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.fields['sub_category'].queryset = SubCategory.objects.none()
            self.fields['sub_category'].required = False
            
            if 'category' in self.data:
                try:
                    category_id = int(self.data.get('category'))
                    self.fields['sub_category'].queryset = SubCategory.objects.filter(category_id=category_id)
                except (ValueError, TypeError):
                    pass
            elif self.instance.pk and self.instance.category:
                self.fields['sub_category'].queryset = self.instance.category.subcategory_set.all()