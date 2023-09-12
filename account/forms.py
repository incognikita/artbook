from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import AuthenticationForm
from .models import Profile


class RegistrationUserForm(forms.ModelForm):
    """Форма регистрации нового пользователя"""
    username = forms.CharField(max_length=150,
                               label='Login',
                               widget=forms.TextInput(attrs={'placeholder': 'login'}))
    email = forms.EmailField(max_length=200,
                             label='Email',
                             widget=forms.TextInput(attrs={'placeholder': 'email@example.com'}))
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput(attrs={'placeholder': 'password'}))
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput(attrs={'placeholder': 'repeat your password'}))

    #  Есть ли пользователь с username в бд или нет.
    def clean_username(self):
        username = self.cleaned_data['username']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Username {username} already in use')
        return username

    #  Есть ли пользователь с email в бд или нет.
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Email already in use')
        return email

    #  Пароли не совпадают
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password dont match')
        return cd['password2']

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']


class LoginUserForm(AuthenticationForm):
    """Форма входа пользователя"""
    username = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'password'}))


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(disabled=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class ProfileEditForm(forms.ModelForm):
    headline = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'one line about you'}))

    class Meta:
        model = Profile
        fields = ['headline', 'date_of_birth', 'gender', 'photo']
        widgets = {
            'date_of_birth': forms.SelectDateWidget(years=range(1940, 2023)),
        }

