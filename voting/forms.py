from .models import Category, Candidate, Election
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
            
            
class VoterUploadForm(forms.Form):
    election = forms.ModelChoiceField(
        queryset=Election.objects.all(),
        empty_label="Select an Election"
    )
    json_file = forms.FileField(
        label='Voter JSON File',
        help_text='Upload a JSON file containing voter data'
    )
    
    # Optional: Add password options
    DEFAULT_PASSWORD = 'default123'  # You can remove this if you always want custom passwords
    
    use_custom_passwords = forms.BooleanField(
        required=False,
        initial=True,
        label='Use passwords from JSON file',
        help_text='If unchecked, a default password will be set for all users'
    )
    
    default_password = forms.CharField(
        required=False,
        initial=DEFAULT_PASSWORD,
        label='Default Password',
        help_text='Password to use if not using custom passwords',
        widget=forms.PasswordInput(render_value=True)
    )
