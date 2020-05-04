from django import forms

from app.models import Nurse


class SignupForm(forms.Form):
    first_name = forms.CharField(
        label='Имя', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Введите имя'}))
    last_name = forms.CharField(
        label='Фамилия', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Введите фамилию'}))
    username = forms.CharField(
        label='Логин', max_length=100, widget=forms.TextInput(attrs={'placeholder': 'Придумайте логин'}))
    password = forms.CharField(
        label='Пароль', max_length=100, widget=forms.PasswordInput(attrs={'placeholder': 'Придумайте пароль'}))

    def clean_username(self):
        uname = self.cleaned_data.get('username')
        if uname and Nurse.objects.filter(username=uname).first():
            raise forms.ValidationError('Такой логин занят')
        return uname

    def save(self):
        return Nurse.objects.create_user(**self.cleaned_data)
