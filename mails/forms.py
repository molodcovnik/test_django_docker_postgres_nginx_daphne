from django import forms
from mails.models import EmailAccount


class EmailAccountForm(forms.ModelForm):
    class Meta:
        model = EmailAccount
        fields = ['email', 'password', 'provider']
        widgets = {
            'password': forms.PasswordInput(),
        }

