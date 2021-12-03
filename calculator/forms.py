# Django imports
from django import forms
from django.forms import widgets

# My file imports
from .models import *

class RentalPropForm(forms.ModelForm):
    """Form for rental property calculator"""
    required_css_class = 'required'
    class Meta:
        model = RentalPropCalcReport
        fields = '__all__'
        widgets = {'owner': forms.HiddenInput()}


class UserSettingsForm(forms.ModelForm):
    """Form for user settings"""
    class Meta:
        model = UserSettings
        fields = '__all__'
        widgets = {'user': forms.HiddenInput()}
