from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password


class AuthenticationFormWithEmail(AuthenticationForm):
    # The field is an EmailField, which validates that the input is a valid email address
    username = forms.EmailField(label='Email')



class forgotpasswordForm(forms.Form):
    email = forms.EmailField(label='Email')


class resetpasswordForm(forms.Form):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

    def clean_password1(self):
        # Get the password from the cleaned data
        password1 = self.cleaned_data.get('password1')
        
        # Validate the password using Django's validators
        try:
            validate_password(password1)
        except ValidationError as e:
            # Add validation errors to the form's password1 field
            self.add_error('password1', e)
        
        # Return the cleaned password
        return password1

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            self.add_error('password2', "Passwords do not match")

        return cleaned_data
    
    
