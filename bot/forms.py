# Django imports
from django import forms

# My file imports
from .models import *

class BotRentalPropForm(forms.ModelForm):
    """Form for bot calculator"""
    required_css_class = 'required'
    class Meta:
        model = BotRentalReport
        fields = '__all__'
        widgets = {'owner': forms.HiddenInput()}
