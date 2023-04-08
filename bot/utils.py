# Django imports
from django.http.response import Http404
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import get_template

# 3rd party imports
import pandas as pd
from datetime import datetime
import pytz
from io import BytesIO
from xhtml2pdf import pisa

# My file imports
from .models import BotRentalReport
from calculator.models import UserSettings
# from .bot import RedfinBot
from calculator.calc import *

closing_cost_percentage = 0.02 # add as setting?


# def run_bot_logic(user):
#     """Runs bot logic"""
#     print('Current time:', datetime.now(tz=pytz.timezone('US/Eastern'))\
#         .strftime("%A, %B %d %Y %H:%M:%S ET (%-I:%M:%S %p)"))
#     try:
#         user_settings = UserSettings.objects.get(user=user)
#         down_payment = user_settings.down_payment
#         loan_int_rate = user_settings.loan_int_rate
#         loan_term = user_settings.loan_term
#         repairs_maint = user_settings.repairs_maint
#         vacancy = user_settings.vacancy
#         cap_expenditures = user_settings.cap_expenditures
#         mgmt_fees = user_settings.mgmt_fees

#     except:
#         down_payment = '0%'
#         loan_int_rate = 0.00
#         loan_term = 0
#         repairs_maint = 0.00
#         vacancy = 0.00
#         cap_expenditures = 0.00
#         mgmt_fees = 0.00


#     report_owner = user
#     data = RedfinBot(user).run()

#     if data: # if data returned from Redfin Bot, clean up some fields
#         for key in data:
#             if pd.isna(data[key]['HOA/MONTH']):
#                 data[key]['HOA/MONTH'] = None
#             if data[key]['HOA/MONTH']:
#                 data[key]['HOA'] = data[key]['HOA/MONTH']
#             if pd.isna(data[key]['YEAR BUILT']):
#                 data[key]['YEAR BUILT'] = ''
#             else:
#                 data[key]['YEAR BUILT'] = str(int(data[key]['YEAR BUILT']))
#             if pd.isna(data[key]['SQUARE FEET']):
#                 data[key]['SQUARE FEET'] = ''

#         # creates list of new objects to be created in database
#         objs = [
#             BotRentalReport(
#                 owner = report_owner,
#                 report_title = data[key]['ADDRESS'],
#                 owned = False,
#                 prop_address = data[key]['ADDRESS'],
#                 prop_city = data[key]['CITY'],
#                 prop_state = data[key]['STATE OR PROVINCE'],
#                 prop_zip = str(data[key]['ZIP OR POSTAL CODE']),
#                 bedrooms = str(int(data[key]['BEDS'])),
#                 bathrooms = str(int(data[key]['BATHS'])),
#                 sqft = str(data[key]['SQUARE FEET']),
#                 year_built = data[key]['YEAR BUILT'],
#                 prop_description = data[key]['DESCRIPTION'],
#                 prop_photo = f"property_photos/{data[key]['IMAGE NAME']}",
#                 prop_mls = str(data[key]['MLS#']),
#                 purchase_price = int(data[key]['PRICE']),
#                 purchase_closing_cost = int(data[key]['PRICE'] * closing_cost_percentage),
#                 after_repair_value = int(data[key]['PRICE']),
#                 cash_purchase = False,
#                 down_payment = down_payment,
#                 loan_int_rate = loan_int_rate,
#                 loan_term = loan_term,
#                 gross_monthly_rent = int(data[key]['ZESTIMATE']),
#                 prop_annual_taxes = int(data[key]['ANNUAL TAXES']),
#                 monthly_insurance = data[key]['HOMEOWNERS INSURANCE'],
#                 repairs_maint = repairs_maint,
#                 vacancy = vacancy,
#                 cap_expenditures = cap_expenditures,
#                 mgmt_fees = mgmt_fees,
#                 hoa = float(data[key]['HOA']),
#                 redfin_listing_url = data[key]['URL (SEE https://www.redfin.com/buy-a-home/comparative-market-analysis FOR INFO ON PRICING)'],
#                 zillow_zestimate_url = data[key]['ZESTIMATE URL']
#             )
#             if not BotRentalReport.objects.filter(owner=report_owner).filter(prop_address=data[key]['ADDRESS']).exists()
#             else None
#             for key in data
#         ]

#         new_reports = list(filter(lambda obj: obj != None, objs))
#         if new_reports:
#             BotRentalReport.objects.bulk_create(new_reports) # creates objects
#             for o in new_reports:
#                 obj = get_object_or_404(BotRentalReport, prop_address=o.prop_address)
#                 context = run_report_calc(obj) # run calculations and retrieve context
#                 coc_roi = context['coc_roi']
#                 cashflow = context['cashflow']
#                 quality  = get_report_quality(user, coc_roi, cashflow)
#                 save_report_quality(obj, quality)
                
#             print(f'{len(new_reports)} new reports created\n')
#         else:
#             print(f'{len(new_reports)} new reports created\n')
#     else:
#         print("0 new reports created\n")

def render_to_pdf(template_src, context_dict={}):
    """renders template data to PDF"""
    template = get_template(template_src)
    html  = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result, encoding='UTF-8')
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None

def run_report_calc(obj):
    """Run report calculations and return context"""
    mo_income = monthly_income(obj.gross_monthly_rent, obj.other_monthly_income)
    total_op_exp = total_operating_expenses(
        mo_income, 
        obj.electricity,
        obj.gas,
        obj.water_sewer,
        obj.pmi,
        obj.garbage,
        obj.hoa,
        obj.monthly_insurance,
        obj.prop_annual_taxes,
        obj.other_monthly_expenses,
        obj.vacancy,
        obj.repairs_maint,
        obj.cap_expenditures,
        obj.mgmt_fees
        )
    dwn_pmt = down_payment(obj.purchase_price, obj.down_payment, obj.down_payment_2)
    dwn_pmt_percent = f'{round((dwn_pmt/obj.purchase_price) * 100, 2):g}'
    loan_amt = loan_amount(obj.purchase_price, dwn_pmt)
    loan_pts = loan_points(obj.purchase_price, obj.points)
    ttl_clos_costs = total_closing_costs(obj.purchase_closing_cost, loan_pts)
    p_i = loan_principal_interest(loan_amt, obj.loan_int_rate, obj.loan_term)
    total_cash = total_cash_needed(dwn_pmt, ttl_clos_costs, obj.est_repair_cost)
    mo_exp = monthly_expenses(total_op_exp, p_i)
    cashflow = monthly_cashflow(mo_income, mo_exp)
    n_o_i = noi(mo_income, total_op_exp)
    purchase_cap_rt = purchase_cap(n_o_i, obj.purchase_price)
    pro_forma_cap_rt = pro_forma_cap(n_o_i, obj.after_repair_value)
    coc_roi = cash_on_cash_ROI(cashflow, total_cash)
    total_cost = total_project_cost(obj.purchase_price, ttl_clos_costs, obj.est_repair_cost)
    aot = analysis_over_time(obj.annual_income_growth, obj.annual_pv_growth, obj.annual_expenses_growth, obj.sales_expenses, obj.loan_term, loan_amt, obj.loan_int_rate, mo_income, total_op_exp, p_i, total_cash, obj.after_repair_value)

    two_pct_rule = two_percent_rule(total_cost, mo_income)
    total_init_equity = total_initial_equity(obj.after_repair_value, obj.purchase_price, dwn_pmt)
    grm = gross_rent_multiplier(mo_income, obj.purchase_price)
    debt_cov_rto = debt_coverage_ratio(n_o_i, p_i)

    context = {
        'obj': obj, 
        'mo_income': mo_income,
        'total_op_exp': total_op_exp,
        'dwn_pmt': dwn_pmt,
        'dwn_pmt_percent': dwn_pmt_percent,
        'loan_amt': loan_amt,
        'loan_pts': loan_pts,
        'ttl_clos_costs': ttl_clos_costs,
        'p_i': p_i,
        'total_cash': total_cash,
        'mo_exp': mo_exp,
        'cashflow': cashflow,
        'n_o_i': n_o_i,
        'purchase_cap_rt': purchase_cap_rt,
        'pro_forma_cap_rt': pro_forma_cap_rt,
        'coc_roi': coc_roi,
        'total_cost': total_cost,
        'aot': aot,

        'two_pct_rule': two_pct_rule,
        'total_init_equity': total_init_equity,
        'grm': grm, 
        'debt_cov_rto': debt_cov_rto
    }

    return context

def get_report_quality(user, coc_roi, cashflow):
    """Returns the report quality based on user settings"""
    user_settings = UserSettings.objects.get(user=user)
    try:
        coc_roi_bottom = user_settings.coc_roi_bottom
        coc_roi_top = user_settings.coc_roi_top
        cashflow_bottom = user_settings.cashflow_bottom
        cashflow_top = user_settings.cashflow_top
    except:
        coc_roi_bottom = None
        coc_roi_top = None
        cashflow_bottom = None
        cashflow_top = None

    if (coc_roi_bottom and coc_roi_top) and (not cashflow_bottom and not cashflow_top):
        if coc_roi >= coc_roi_top:
            return 'good'
        elif coc_roi <= coc_roi_bottom:
            return 'bad'
        else:
            return 'average' 

    if (cashflow_bottom and cashflow_top) and (not coc_roi_bottom and not coc_roi_top):
        if cashflow >= cashflow_top:
            return 'good'
        elif cashflow <= cashflow_bottom:
            return 'bad'
        else:
            return 'average' 

    if (coc_roi_bottom and coc_roi_top) and (cashflow_bottom and cashflow_top):
        if coc_roi >= coc_roi_top and cashflow >= cashflow_top:
            return 'good'
        elif coc_roi <= coc_roi_bottom and cashflow <= cashflow_bottom:
            return 'bad'
        else:
            return 'average'    

def save_report_quality(obj, quality):
    """Saves the object quality"""
    if quality == 'good':
        obj.quality_g = True
        obj.quality_a = False
        obj.quality_b = False
    elif quality == 'average':
        obj.quality_g = False
        obj.quality_a = True
        obj.quality_b = False
    elif quality == 'bad':
        obj.quality_g = False
        obj.quality_a = False
        obj.quality_b = True
    obj.save()

class ProcessReportMixin:
    """Processes data to display on report page"""
    model = None
    template = None

    def get(self, request, pk, *args, **kwargs):
        obj = get_object_or_404(self.model, pk=pk)

        if obj.owner != request.user:
            raise Http404

        context = run_report_calc(obj) # run calculations and retrieve context
        coc_roi = context['coc_roi']
        cashflow = context['cashflow']
        quality  = get_report_quality(request.user, coc_roi, cashflow)
        save_report_quality(obj, quality)

        return render(request, self.template, context)
    
        
class CreatePdfMixin:
    """Creates PDF of report data"""
    model = None
    template = None

    def get(self, request, pk, *args, **kwargs):
        """Retrieves model based on pk if any, else raises 404"""
        obj = get_object_or_404(self.model, pk=pk)

        if obj.owner != request.user:
            raise Http404
            
        context = run_report_calc(obj) # run calculations and retrieve context
        
        # reads expense report, gathers relevant non "nan" data and puts them
        # in context for rendering
        exp_report = pd.read_csv('expense_report.csv', index_col=0)
        exp_pie_nums = []
        for x in exp_report['expense']:
            value = exp_report.loc[exp_report['expense'] == x, '$'].iloc[0]
            if not pd.isna(value):
                exp_pie_nums.append({"expense": x, "amount": str(value)})

        # reads income report, gathers relevant non "nan" data and puts them
        # in context for rendering
        inc_report = pd.read_csv('income_report.csv', index_col=0)
        inc_pie_nums = []
        for x in inc_report['income']:
            value = inc_report.loc[inc_report['income'] == x, '$'].iloc[0]
            if not pd.isna(value):
                inc_pie_nums.append({"income": x, "amount": str(value)})

        context['exp_pie_nums'] = exp_pie_nums
        context['inc_pie_nums'] = inc_pie_nums
        coc_roi = context['coc_roi']
        cashflow = context['cashflow']
        quality  = get_report_quality(request.user, coc_roi, cashflow)
        context['quality'] = quality

        pdf = render_to_pdf(self.template, context)
        pdf.getvalue()

        if pdf:
            response = HttpResponse(pdf, content_type="application/pdf")

            # names pdf file 
            pdf_name = f'{obj.report_title.lower().replace(" ","_")}_'\
                    f'{pk}.pdf'
            content = f'inline; filename={pdf_name}'
            response['Content-Disposition'] = content
            return response

        else:
            return redirect(f'/report/{pk}')