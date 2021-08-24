from django import forms
from django.contrib.auth.models import User
SIZE_CHOISES = (
    (1, "5MB"),
    (2, "10MB")
)
SERVER_CHOISES = (
    (1, "Server 1"),
    (2, "Server 2"))
MODES=(
    (1, "Random server"),
    (2, "Selective server testing"),
    (3, "Download testing by data package")
)
class SizeForm(forms.Form):
    sizechoise = forms.ChoiceField(widget=forms.RadioSelect, choices= SIZE_CHOISES)

class ServerChoise(forms.Form):
    serverchoise = forms.ChoiceField(widget=forms.RadioSelect, choices= SERVER_CHOISES)
class WorkMode(forms.Form):
    mode = forms.ChoiceField(widget=forms.RadioSelect,choices=MODES)

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords don\'t match.')
        return cd['password2']


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('username','email')
