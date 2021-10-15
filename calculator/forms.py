from django import forms
from .models import *

class RentalPropForm(forms.ModelForm):
    required_css_class = 'required'
    class Meta:
        model = RentalPropCalcReport
        fields = '__all__'
