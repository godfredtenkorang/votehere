from .models import Category, Candidate
from django import forms



class VoteForm(forms.Form):
    def __init__(self, election, *args, **kwargs):
        super(VoteForm, self).__init__(*args, **kwargs)
        
         # Get categories ordered properly
        categories = Category.objects.filter(election=election).order_by('order')
        
        for category in categories:
            field_name = f'category_{category.id}'  # Consistent field naming
            self.fields[field_name] = forms.ModelChoiceField(
                queryset=Candidate.objects.filter(category=category).order_by('order'),
                widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
                empty_label=None,
                label=category.name,
                required=True
            )
            
            # Add photo and bio to choices
            field = self.fields[f'category_{category.id}']
            field.label_from_instance = lambda obj: obj  # Pass whole object
            
            
