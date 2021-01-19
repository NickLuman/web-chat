from django import forms
from django.contrib.auth.models import User

from .models import Message

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password_repeat = forms.CharField(label='Repeat password',
                                      widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)
    
    def clean_password_repeat(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password_repeat']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password_repeat']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['message']
        labels = {'message': ""}