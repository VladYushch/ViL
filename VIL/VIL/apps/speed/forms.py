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
