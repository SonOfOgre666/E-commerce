from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Customer
from django.contrib.auth.models import User


class UserRegistrationForm(forms.ModelForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","type": "text",}),label="First name")
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","type": "text",}),label="Last name")
    username = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","type": "text",}),label="Username")
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": "form-control","type": "email",}),label="Email")
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control","type": "password",}),label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"class": "form-control","type": "password",}),label="Confirm Password")
    age = forms.CharField(widget=forms.NumberInput(attrs={"class": "form-control","type": "number",}),label="Age")
    country = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","type": "text",}),label="Country")
    city = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","type": "text",}),label="City")
    phone = forms.CharField(widget=forms.TextInput(attrs={"class": "form-control","type": "text",}),label="Phone")
    gender = forms.CharField(widget=forms.Select(choices=(('M', 'Male'), ('F', 'Female'), ('O', 'Other'))))

    class Meta:
        model = Customer
        fields = ['username', 'first_name', 'last_name', 'email', 'age', 'country', 'city', 'phone', 'gender']
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=False)
        password = self.cleaned_data["password1"]
        user.set_password(password)
        if commit:
            user.save()
        return user

