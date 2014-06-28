from django import forms

from forum.models import ForumUser

class LoginForm(forms.Form):
    username = forms.CharField(min_length=4)
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=28)
    
class RegisterForm(forms.Form):
    username = forms.CharField(min_length=4)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=28)
    
class ProfileForm(forms.ModelForm):
    class Meta:
        model = ForumUser
        fields = ['username', 'first_name', 'last_name', 'email', 'date_joined', 'gender', 'city', 'birth_date']
        
class ProfileChangeForm(forms.ModelForm):
    class Meta:
        model = ForumUser
        fields = ['first_name', 'last_name', 'gender', 'city', 'birth_date']
    
class NewContentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}), min_length=1)
    
class SearchForm(forms.Form):
    types = [
        ('post', 'съдържание'),
        ('topic', 'заглавие'),
        ('category', 'категория'),
    ]
    search_field = forms.CharField(min_length=2)
    type = forms.ChoiceField(choices=types)
    author_username = forms.CharField(required=False)
    date_field = forms.DateField(required=False)