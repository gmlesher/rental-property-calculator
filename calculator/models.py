# Django imports
from django.db import models
from django.contrib.auth.models import User

# 3rd party imports
from multiselectfield import MultiSelectField

# My file imports
from .choices import *

class UserSettings(models.Model):
    """Model for storing user calculator and bot settings"""
    user                = models.OneToOneField(User, on_delete=models.CASCADE, related_name='settings')

    # Calculator Settings
    down_payment        = models.CharField(max_length=10, \
                                choices=DOWN_PMT_PERCENT, default='', blank=True)
    loan_int_rate       = models.DecimalField(max_digits=5, decimal_places=3, \
                            blank=True, null=True)
    loan_term           = models.SmallIntegerField(blank=True, null=True)
    repairs_maint       = models.DecimalField(max_digits=4, decimal_places=2, \
                            blank=True, null=True)
    vacancy             = models.DecimalField(max_digits=4, decimal_places=2, \
                            blank=True, null=True)
    cap_expenditures    = models.DecimalField(max_digits=4, decimal_places=2, \
                            blank=True, null=True)
    mgmt_fees           = models.DecimalField(max_digits=4, decimal_places=2, \
                            blank=True, null=True)

    # Investment Quality Settings
    coc_roi_bottom      = models.DecimalField(max_digits=4, decimal_places=2, \
                            blank=True, null=True)
    coc_roi_top         = models.DecimalField(max_digits=4, decimal_places=2, \
                            blank=True, null=True)
    cashflow_bottom      = models.SmallIntegerField(blank=True, null=True)
    cashflow_top         = models.SmallIntegerField(blank=True, null=True)

    # Bot Settings
    city                = models.CharField(max_length=30, blank=True)
    state               = models.CharField(max_length=10, \
                                choices=STATES, default='', blank=True)
    city_code           = models.CharField(max_length=10, blank=True)                       
    minor_civil_div     = models.BooleanField(blank=True, default=False)
    zipcode             = models.CharField(max_length=5, blank=True)

    # Bot Filters
    min_price           = models.CharField(max_length=10, \
                                choices=BOT_MIN_PRICE, default='', blank=True)
    max_price           = models.CharField(max_length=10, \
                                choices=BOT_MAX_PRICE, default='', blank=True)
    prop_type           = MultiSelectField(max_length=100, \
                                choices=PROPERTY_TYPES, default=None, blank=True)
    min_beds            = models.CharField(max_length=10, \
                                choices=BOT_MIN_BEDS, default='', blank=True)
    max_beds            = models.CharField(max_length=10, \
                                choices=BOT_MAX_BEDS, default='', blank=True)
    min_baths           = models.CharField(max_length=10, \
                                choices=BOT_MIN_BATHS, default='', blank=True)

    # Bot Schedule
    bot_frequency       = models.CharField(max_length=100, \
                                choices=BOT_FREQUENCY, default='', blank=True)

    # Address Blacklist
    blacklist_bool      = models.BooleanField(blank=True)
    addr_blacklist      = models.JSONField(blank=True)

    def __str__(self):
        """Return a string representation of the model"""
        return f'{self.user}' + ' settings'

    def save(self, *args, **kwargs):
        """Saves model"""
        if self.city and self.city_code and self.state:
            self.zipcode = ''
        if self.zipcode:
            self.city = ''
            self.city_code = '' 
            self.state = ''
        super(UserSettings, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "User Settings"


class RentalPropCalcReport(models.Model):
    """A rental property report the user would like to create"""
    created_at              = models.DateTimeField(auto_now_add=True)
    updated_at              = models.DateTimeField(auto_now=True)
    owner                   = models.ForeignKey(User, on_delete=models.CASCADE, \
                                blank=True, null=True)
    # quality of investment
    quality_g               = models.BooleanField(blank=True, default=False)
    quality_a               = models.BooleanField(blank=True, default=False)
    quality_b               = models.BooleanField(blank=True, default=False)

    # Property Info
    listing_url             = models.URLField(blank=True)
    report_title            = models.CharField(max_length=75)
    owned                   = models.BooleanField(blank=True)
    prop_address            = models.CharField(max_length=75, blank=True)
    prop_city               = models.CharField(max_length=50, blank=True)
    prop_state              = models.CharField(max_length=10, \
                                choices=STATES, default='', blank=True)
    prop_zip                = models.CharField(max_length=10, blank=True, \
                                verbose_name='Zip')
    bedrooms                = models.CharField(max_length=10, \
                                choices=BEDROOMS, default='', blank=True)
    bathrooms               = models.CharField(max_length=10, \
                                choices=BATHROOMS, default='', blank=True)
    sqft                    = models.CharField(max_length=30, blank=True)
    year_built              = models.CharField(max_length=4, blank=True)
    prop_description        = models.TextField(blank=True)
    prop_photo              = models.ImageField(upload_to='property_photos', blank=True)
    prop_mls                = models.CharField(max_length=30, blank=True)
    
    # Purchase Info 
    purchase_price          = models.IntegerField()
    purchase_closing_cost   = models.IntegerField()
    est_repair_cost         = models.IntegerField(blank=True, null=True)
    after_repair_value      = models.IntegerField(blank=True, null=True)
    annual_pv_growth        = models.DecimalField(max_digits=4, decimal_places=2, \
                                blank=True, null=True, default=2)

    # Loan Details
    cash_purchase           = models.BooleanField(blank=True)
    down_payment            = models.CharField(max_length=10, \
                                choices=DOWN_PMT_PERCENT, default='', blank=True)
    down_payment_2          = models.IntegerField(blank=True, null=True)
    loan_int_rate           = models.DecimalField(max_digits=5, decimal_places=3)
    points                  = models.SmallIntegerField(blank=True, null=True)
    loan_term               = models.SmallIntegerField()

    # Rental Income
    gross_monthly_rent      = models.SmallIntegerField()
    other_monthly_income    = models.SmallIntegerField(blank=True, null=True)
    annual_income_growth    = models.DecimalField(max_digits=4, decimal_places=2, \
                                blank=True, null=True, default=2)

    # Expenses
    prop_annual_taxes       = models.IntegerField()
    monthly_insurance       = models.DecimalField(max_digits=7, decimal_places=2)
    repairs_maint           = models.DecimalField(max_digits=4, decimal_places=2, \
                                blank=True, null=True)
    vacancy                 = models.DecimalField(max_digits=4, decimal_places=2, \
                                blank=True, null=True)
    cap_expenditures        = models.DecimalField(max_digits=4, decimal_places=2, \
                                blank=True, null=True)
    mgmt_fees               = models.DecimalField(max_digits=4, decimal_places=2, \
                                blank=True, null=True)
    electricity             = models.DecimalField(max_digits=7, decimal_places=2, \
                                blank=True, null=True)
    gas                     = models.DecimalField(max_digits=7, decimal_places=2, \
                                blank=True, null=True)
    water_sewer             = models.DecimalField(max_digits=7, decimal_places=2, \
                                blank=True, null=True)
    hoa                     = models.DecimalField(max_digits=7, decimal_places=2, \
                                blank=True, null=True)
    garbage                 = models.DecimalField(max_digits=7, decimal_places=2, \
                                blank=True, null=True)
    pmi                     = models.DecimalField(max_digits=7, decimal_places=2, \
                                blank=True, null=True)
    other_monthly_expenses  = models.DecimalField(max_digits=7, decimal_places=2, \
                                blank=True, null=True)
    annual_expenses_growth  = models.DecimalField(max_digits=4, decimal_places=2, \
                                blank=True, null=True, default=2)
    sales_expenses          = models.DecimalField(max_digits=4, decimal_places=2, \
                                blank=True, null=True, default=7.5)

    def __str__(self):
        """Return a string representation of the model"""
        return self.report_title + ' - ' + self.owner.username + f' ({str(self.id)})'

    def save(self, *args, **kwargs):
        """Saves model. Sets ARV equal to purchase price if ARV is blank"""
        if self.after_repair_value == None:
            self.after_repair_value = self.purchase_price
        super(RentalPropCalcReport, self).save(*args, **kwargs)