from django import forms
from django.contrib.auth import get_user_model
from .models import Profile
from django.contrib.auth.models import User



class LoginForm(forms.Form):
    #username = forms.CharField(max_length=150, required=True, label='Username')
    #password = forms.CharField(widget=forms.PasswordInput, required=True, label='Password')
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Repeat Password')

    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'email')

def clean_password2(self):
    cd = self.cleaned_data
    if cd['password'] != cd['password2']:
        raise forms.ValidationError("Passwords don't match.")
    return cd['password2']

class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'email')

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError("A user with that email already exists.")
        return data

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'bio', 'location', 'photo')
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 3}),
            'location': forms.TextInput(attrs={'placeholder': 'City, Country'}),
        }

def clean_email(self):
    data = self.cleaned_data['email']
    if User.objects.filter(email=data).exists():
        raise forms.ValidationError("A user with that email already exists.")
    return data