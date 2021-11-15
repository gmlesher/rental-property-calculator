import pandas as pd
import schedule, time

# my files
from .models import BotRentalReport
from calculator.models import UserSettings
from .bot import RedfinBot

def bot_scheduler(user):
    settings = UserSettings.objects.get(user=user)
    # every hour
    if settings.bot_frequency == "Every hour":
        schedule.every().hour.at(":00").do(run_bot_logic, user)

    # every 6 hours
    if settings.bot_frequency == "Every 6 hours":
        schedule.every().day.at("00:00").do(run_bot_logic, user)
        schedule.every().day.at("06:00").do(run_bot_logic, user)
        schedule.every().day.at("12:00").do(run_bot_logic, user)
        schedule.every().day.at("18:00").do(run_bot_logic, user)

    # every 12 hours
    if settings.bot_frequency == "2x/day":
        schedule.every().day.at("00:00").do(run_bot_logic, user)
        schedule.every().day.at("12:00").do(run_bot_logic, user)
    
    # 1/day
    if settings.bot_frequency == "1x/day":
        schedule.every().day.at("17:00").do(run_bot_logic, user)
    
    # every other day
    if settings.bot_frequency == "Every other day":
        schedule.every(2).days.at("17:00").do(run_bot_logic, user)

    # 1/week
    if settings.bot_frequency == "1x/week":
        schedule.every().week.do(run_bot_logic, user)

    # 1/month
    if settings.bot_frequency == "1x/month":
        schedule.every(4).weeks.do(run_bot_logic, user)
    
    while True:
        schedule.run_pending()
        time.sleep(1)


def run_bot_logic(user):
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
                year_built = str(int(data[key]['YEAR BUILT'])),
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
                redfin_listing_url = data[key]['URL (SEE http://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)'],
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

