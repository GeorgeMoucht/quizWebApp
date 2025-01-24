from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, label='Όνομα', widget=forms.TextInput(attrs={'placeholder': 'Όνομα'}))
    last_name = forms.CharField(max_length=30, required=True, label='Επώνυμο', widget=forms.TextInput(attrs={'placeholder': 'Επώνυμο'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'Email'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Κωδικός πρόσβασης'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Επαναλάβετε τον κωδικό'}))

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[α-ωΑ-Ωa-zA-Z]+$', first_name):
            raise forms.ValidationError("Το όνομα μπορεί να περιέχει μόνο γράμματα.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[α-ωΑ-Ωa-zA-Z]+$', last_name):
            raise forms.ValidationError("Το επώνυμο μπορεί να περιέχει μόνο γράμματα.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Αυτό το email υπάρχει ήδη.")
        return email

        