import pandas as pd
from datetime import datetime
import pytz

# my files
from .models import BotRentalReport
from calculator.models import UserSettings
from .bot import RedfinBot


def run_bot_logic(user):
    print('Current time:', datetime.now(tz=pytz.timezone('US/Eastern')).strftime("%A, %B %d %Y %H:%M:%S ET (%-I:%M:%S %p)"))
    try:
        user_settings = UserSettings.objects.get(user=user)
        down_payment = user_settings.down_payment
        loan_int_rate = user_settings.loan_int_rate
        loan_term = user_settings.loan_term
        repairs_maint = user_settings.repairs_maint
        vacancy = user_settings.vacancy
        cap_expenditures = user_settings.cap_expenditures
        mgmt_fees = user_settings.mgmt_fees

    except:
        down_payment = '0%'
        loan_int_rate = 0.00
        loan_term = 0
        repairs_maint = 0.00
        vacancy = 0.00
        cap_expenditures = 0.00
        mgmt_fees = 0.00


    report_owner = user
    data = RedfinBot(user).run()

    if data:
        for key in data:
            if pd.isna(data[key]['HOA/MONTH']):
                data[key]['HOA/MONTH'] = None
            if data[key]['HOA/MONTH']:
                data[key]['HOA'] = data[key]['HOA/MONTH']
            if pd.isna(data[key]['YEAR BUILT']):
                data[key]['YEAR BUILT'] = ''
            else:
                data[key]['YEAR BUILT'] = str(int(data[key]['YEAR BUILT']))
            if pd.isna(data[key]['SQUARE FEET']):
                data[key]['SQUARE FEET'] = ''

        objs = [
            BotRentalReport(
                owner = report_owner,
                report_title = data[key]['ADDRESS'],
                owned = False,
                prop_address = data[key]['ADDRESS'],
                prop_city = data[key]['CITY'],
                prop_state = data[key]['STATE OR PROVINCE'],
                prop_zip = str(data[key]['ZIP OR POSTAL CODE']),
                bedrooms = str(int(data[key]['BEDS'])),
                bathrooms = str(int(data[key]['BATHS'])),
                sqft = str(data[key]['SQUARE FEET']),
                year_built = data[key]['YEAR BUILT'],
                prop_description = data[key]['DESCRIPTION'],
                prop_photo = f"property_photos/{data[key]['IMAGE NAME']}",
                prop_mls = str(data[key]['MLS#']),
                purchase_price = int(data[key]['PRICE']),
                purchase_closing_cost = int(data[key]['PRICE'] * 0.05),
                after_repair_value = int(data[key]['PRICE']),
                cash_purchase = False,
                down_payment = down_payment,
                loan_int_rate = loan_int_rate,
                loan_term = loan_term,
                gross_monthly_rent = int(data[key]['ZESTIMATE']),
                prop_annual_taxes = int(data[key]['ANNUAL TAXES']),
                monthly_insurance = data[key]['HOMEOWNERS INSURANCE'],
                repairs_maint = repairs_maint,
                vacancy = vacancy,
                cap_expenditures = cap_expenditures,
                mgmt_fees = mgmt_fees,
                hoa = float(data[key]['HOA']),
                redfin_listing_url = data[key]['URL (SEE https://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)'],
                zillow_zestimate_url = data[key]['ZESTIMATE URL']
            )
            if not BotRentalReport.objects.filter(owner=report_owner).filter(prop_address=data[key]['ADDRESS']).exists()
            else None
            for key in data
        ]

        new_reports = list(filter(lambda obj: obj != None, objs))
        if new_reports:
            BotRentalReport.objects.bulk_create(new_reports)
            print(f'{len(new_reports)} new reports created')
        else:
            print(f'{len(new_reports)} new reports created')
    else:
        print("0 new reports created")