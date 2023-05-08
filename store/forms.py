from django import forms
from .models import Contact
from django.core.validators import RegexValidator

phone_validator = RegexValidator(
    r"((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))", "Your number must be (xxx)xxxxxxxxx or 0xxxxxxxxx!"
)

class FormContact(forms.ModelForm):
    name = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'placeholder': 'Enter your name',
        'class': 'form-control',
    }))
    phone_number = forms.CharField(max_length=20, validators=[phone_validator], widget=forms.TextInput(
        attrs={ 'placeholder': "Phone number",
            'class': "form-control fh5co_contact_text_box",
            'pattern': "((\([0-9]{3}\)[0-9]{9,15})|([0-9]{10,15}))",
            'title': "Your phone number must be (xxx)xxxxxxxxx or 0xxxxxxxxx"}
    ))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'Email',
        'class': 'form-control fh5co_contact_text_box',
    }))
    subject = forms.CharField(max_length=150, widget=forms.TextInput(attrs={
        'placeholder': 'Subject',
        'class': 'form-control fh5co_contact_text_box',
    }))
    message = forms.CharField(widget=forms.Textarea(attrs={
        'placeholder': 'Message',
        'class': 'form-control fh5co_contact_text_message',
    }))

    class Meta:
        model = Contact
        fields = ['name', 'phone_number', 'email', 'subject', 'message']
        # exclude = ['created']