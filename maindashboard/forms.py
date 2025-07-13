from django import forms

from payment.models import Nominees
from vote.models import Blog, SubCategory

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