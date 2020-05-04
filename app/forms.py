from django import forms

from app.models import Nurse


class SignupForm(forms.Form):
    first_name = forms.CharField(label='Имя', max_length=100)
    last_name = forms.CharField(label='Фамилия', max_length=100)
    username = forms.CharField(label='Логин', max_length=100)
    password = forms.CharField(label='Пароль', max_length=100, widget=forms.PasswordInput())

    def save(self):
        return Nurse.objects.create_user(**self.cleaned_data)
