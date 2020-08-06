from django import forms
from .models import *
class ProfileCreationForm(forms.ModelForm):
    class Meta:
        model=Profile
        fields=('phone_number','about','photo','city','hobby')