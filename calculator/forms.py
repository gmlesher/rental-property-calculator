from django import forms
from django.forms import widgets
from .models import *

class RentalPropForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = RentalPropCalcReport
        fields = '__all__'
        widgets = {'owner': forms.HiddenInput()}


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = UserSettings
        fields = '__all__'
        widgets = {'user': forms.HiddenInput()}
