from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm, UserChangeForm
from django.contrib.auth.models import User

class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(
               attrs={'placeholder': "Логин", "class": "form-control"}))
    password1 = forms.CharField(label="Пароль", widget=forms.PasswordInput(
                attrs={'placeholder': "Пароль", "class": "form-control"}))
    password2 = forms.CharField(label="Повторите пароль", widget=forms.PasswordInput(
                attrs={'placeholder': "Повтор пароля", "class": "form-control"}))
    
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(
               attrs={'placeholder': "Логин", "class": "form-control"}))
    password = forms.CharField(label="Пароль", widget=forms.PasswordInput(
               attrs={'placeholder': "Пароль", "class": "form-control"}))

class ChangePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль", widget=forms.PasswordInput(
                   attrs={'placeholder': "Старый пароль", "class": "form-control"}))
    new_password1 = forms.CharField(label="Новый пароль", widget=forms.PasswordInput(
                    attrs={'placeholder': "Новый пароль", "class": "form-control"}))
    new_password2 = forms.CharField(label="Подтверждение нового пароля", widget=forms.PasswordInput(
                    attrs={'placeholder': "Повтор нового пароля", "class": "form-control"}))
    
    class Meta:
        model = User
        fields = ('old_password', 'new_password1', 'new_password2')

class ChangeUserDataForm(UserChangeForm):
    username = forms.CharField(label="Логин", widget=forms.TextInput(
               attrs={'placeholder': "Введите логин", "class": "form-control"}))
    first_name = forms.CharField(label="Имя", required=False, widget=forms.TextInput(
                 attrs={'placeholder': "Введите имя", "class": "form-control"}))
    last_name = forms.CharField(label="Фамилия", required=False, widget=forms.TextInput(
                attrs={'placeholder': "Введите фамилию", "class": "form-control"}))
    email = forms.EmailField(label="Электронная почта", required=False, widget=forms.EmailInput(
            attrs={'placeholder': "Введите электронную почту", "class": "form-control"}))
    password = None
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
