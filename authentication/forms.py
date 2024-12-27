from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
import re


class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True,label='Όνομα')
    last_name = forms.CharField(max_length=30, required=True,label='Επώνυμο')
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
    
    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if not re.match(r'^[α-ωΑ-Ω]+$', first_name):
            raise forms.ValidationError("Το όνομα μπορεί να περιέχει μόνο γράμματα.")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        if not re.match(r'^[α-ωΑ-Ω]+$', last_name):
            raise forms.ValidationError("Το επώνυμο μπορεί να περιέχει μόνο γράμματα.")
        return last_name

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Αυτό το email υπάρχει ήδη.")
        return email

        