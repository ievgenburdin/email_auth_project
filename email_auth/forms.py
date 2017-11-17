from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.EmailField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class LoginForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'password')


class ChangeForm(forms.ModelForm):
    username = forms.CharField(required=False)
    email = forms.EmailField(widget=forms.EmailInput(),
                             required=False)
    password = forms.CharField(widget=forms.PasswordInput(),
                               required=False)
    new_password = forms.CharField(widget=forms.PasswordInput(),
                                   required=False)
    repeat_new_password = forms.CharField(widget=forms.PasswordInput(),
                                          required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

