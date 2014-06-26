from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(min_length=4)
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=28)
    
class RegisterForm(forms.Form):
    username = forms.CharField(min_length=4)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput, min_length=6, max_length=28)
    
class ProfileForm(forms.Form):
    username = forms.CharField(min_length=4)
    first_name = forms.CharField(min_length=4)
    last_name = forms.CharField(min_length=4)
    email = forms.EmailField()
    date_joined = forms.DateTimeField()
    picture = forms.ImageField()
    gender = forms.ChoiceField()
    city = forms.CharField()
    birth_date = forms.DateField()
    
class NewContentForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea, min_length=1)
    
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