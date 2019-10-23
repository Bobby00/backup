from django import forms
from allauth.account.forms import LoginForm, SignupForm

class LoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['login'] = forms.CharField(widget=forms.TextInput(attrs={'class': 'cstm_brder', 'placeholder':'Enter your email'}), label='')
        self.fields['password'] = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'cstm_brder', 'placeholder':'Your Password'}), label='')


class SignupForm(SignupForm):
    def __init__(self, *args, **kwargs):
        super(SignupForm, self).__init__(*args, **kwargs)
        self.fields['username'] = forms.CharField(widget=forms.TextInput(attrs={'class': 'cstm_brder', 'placeholder':'Enter your username'}), label='')
        self.fields['email'] = forms.CharField(widget=forms.EmailInput(attrs={'class': 'cstm_brder', 'placeholder':'Enter your email'}), label='')
        self.fields['password1'] = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'cstm_brder', 'placeholder':'Your Password'}), label='')
        self.fields['password2'] = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'cstm_brder', 'placeholder':'Confirm Password'}), label='')


