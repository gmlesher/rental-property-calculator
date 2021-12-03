# Django imports
from django.contrib import admin

# My file imports
from .models import *

admin.site.register(RentalPropCalcReport)
admin.site.register(UserSettings)