from django.core.exceptions import ValidationError
from django.forms import Form, CharField, ModelForm, PasswordInput, EmailField, forms

from apps.models import User


class EmailForm(Form):
    email = CharField(max_length=255)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        query = User.objects.filter(email=email)
        if query.exists():
            raise ValidationError(f'{email} exists')
        return email


class RegisterModelForm(ModelForm):
    password = CharField(widget=PasswordInput())
    password_confirm = CharField(widget=PasswordInput())
    sms = CharField(label='SMS Code')
    email = EmailField()

    class Meta:
        model = User
        fields = ['email', 'sms', 'password', 'password_confirm']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            raise ValidationError("Passwords do not match.")
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(Form):
    email = CharField(max_length=255)
    password = CharField(max_length=255)





