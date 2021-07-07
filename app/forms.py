from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from app.models import Profile

class RegistertionForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("name","address", "city","state","zip")
        widgets = {'name':forms.TextInput(),
                    "address1":forms.TextInput(),
                    "address2":forms.TextInput(),
                    "city":forms.TextInput(),
                    "state":forms.Select(),
                    "zip":forms.NumberInput()}
