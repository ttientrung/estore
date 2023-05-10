from django import forms
from customer.models import Customer


class FormDangKy(forms.ModelForm):
    first_name = forms.CharField(max_length=264, label='First Name', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "First Name",
    }))
    last_name = forms.CharField(max_length=264, label='Last Name', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Last Name",
    }))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Email",
    }))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Password",
    }))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Confirm Password",
    }))
    phone = forms.CharField(max_length=20, label='Phone', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Phone",
    }))
    address = forms.CharField(label='Address', widget=forms.Textarea(attrs={
        "class": "form-control", "placeholder": "Address", "rows": "3",
    }))
    province = forms.CharField(label='Province', widget=forms.Select(attrs={
        "class": "form-control",
    }))
    district = forms.CharField(label='District', widget=forms.Select(attrs={
        "class": "form-control",
    }))
    ward = forms.CharField(label='Ward', widget=forms.Select(attrs={
        "class": "form-control",
    }))

    class Meta:
        model = Customer
        fields = '__all__'

class UpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=264, label='First Name', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "First Name",
    }))
    last_name = forms.CharField(max_length=264, label='Last Name', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Last Name",
    }))
    email = forms.EmailField(label='Email', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Email", 'readonly':'readonly'
    }))
    phone = forms.CharField(max_length=20, label='Phone', widget=forms.TextInput(attrs={
        "class": "form-control", "placeholder": "Phone",
    }))
    address = forms.CharField(label='Address', widget=forms.Textarea(attrs={
        "class": "form-control", "placeholder": "Address", "rows": "3",
    }))

    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone', 'address']

class PassChangeForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Password",
    }))
    confirm_password = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        "class": "form-control", "placeholder": "Confirm Password",
    }))

    class Meta:
        model = Customer
        fields = ['password', 'confirm_password']