from django import forms
from django.forms import widgets

from .models import Contact


class ContactForm(forms.ModelForm):

    class Meta:
        model = Contact
        fields = ('email',)
        widgets = {
            'email': forms.TextInput(attrs={'class': "form-control email-box",
            'placeholder': "email@example.com"})
        }
        labels = {
            'email':'',
        }
