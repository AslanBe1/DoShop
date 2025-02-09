from django import forms

from User.models import User


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if not email:
            raise forms.ValidationError("Email empty")

        if not User.objects.filter(email=email).exists():
            raise forms.ValidationError("User does not exist")
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        if not password:
            raise forms.ValidationError("User does not exist")
        return password

    def clean(self):
        email = self.cleaned_data.get('email')
