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


class RegisterForm(forms.ModelForm):
    email = forms.EmailField(required=True)
    username = forms.CharField(max_length=150,required=False)
    confirm_password = forms.CharField()

    class Meta:
        model = User
        fields = ['email', 'username', 'confirm_password', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if email is None:
            raise forms.ValidationError("Email empty")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError(f"User {email} already exists")
        return email


    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data