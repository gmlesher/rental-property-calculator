from django import forms
from .models import *

class BotRentalPropForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = BotRentalReport
        fields = '__all__'
        widgets = {'owner': forms.HiddenInput()}
