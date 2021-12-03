from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.views.generic import ListView, View


# My files
from .models import RentalPropCalcReport, UserSettings
from bot.utils import CreatePdfMixin, ProcessReportMixin
from bot.crons import clear_crons, make_crons
from .forms import RentalPropForm, UserSettingsForm
from .calc import *

# must be here although not explicitly called in code. registers plotly apps in views
from . import plotly_app

def index(request):
    """The home page for the Rental Property Calculator."""
    return render(request, 'calculator/index.html')

@login_required
def dashboard(request):
    """The dashboard page for a user. Filtered by owned properties for reports"""
    reports = RentalPropCalcReport.objects.filter(owner=request.user).filter(owned=True)
    portfolio_values = [getattr(report, "after_repair_value") for report in reports]
    portfolio_value = sum(portfolio_values)

    purchase_prices = [getattr(report, "purchase_price") for report in reports]
    down_payments_percentage = [getattr(report, "down_payment") for report in reports]
    down_payments_2 = [getattr(report, "down_payment_2") for report in reports]
    
    down_payment_groups = list(zip(purchase_prices, down_payments_percentage, down_payments_2))
    down_payments_amounts = [down_payment(group[0], group[1], group[2]) for group in down_payment_groups]
    
    loan_calc_groups = list(zip(purchase_prices, down_payments_amounts))
    debt_values = [loan_amount(group[0], group[1]) for group in loan_calc_groups]
    debt = sum(debt_values)
    
    total_equity_values = aot_equity(portfolio_values, debt_values)
    total_equity = sum(total_equity_values)

    mnthly_income = [getattr(report, 'gross_monthly_rent') for report in reports]
    othr_income = [getattr(report, 'other_monthly_income') for report in reports]

    monthly_incomes_values = list(zip(mnthly_income, othr_income))
    total_monthly_incomes = [monthly_income(group[0], group[1]) for group in monthly_incomes_values]
    total_monthly_income = sum(total_monthly_incomes)

    elec = [getattr(report, "electricity") for report in reports]
    gas = [getattr(report, "gas") for report in reports]
    water_sewer = [getattr(report, "water_sewer") for report in reports]
    pmi = [getattr(report, "pmi") for report in reports]
    garbage = [getattr(report, "garbage") for report in reports]
    hoa = [getattr(report, "hoa") for report in reports]
    insurance = [getattr(report, "monthly_insurance") for report in reports]
    tax = [getattr(report, "prop_annual_taxes") for report in reports]
    other_expenses = [getattr(report, "other_monthly_expenses") for report in reports]
    vacancy = [getattr(report, "vacancy") for report in reports]
    repairs = [getattr(report, "repairs_maint") for report in reports]
    cap_ex = [getattr(report, "cap_expenditures") for report in reports]
    mgmt_fees = [getattr(report, "mgmt_fees") for report in reports]

    op_ex = list(zip(
        total_monthly_incomes, 
        elec,
        gas,
        water_sewer,
        pmi,
        garbage,
        hoa,
        insurance,
        tax,
        other_expenses,
        vacancy,
        repairs,
        cap_ex,
        mgmt_fees
        ))
    expenses = [total_operating_expenses(
        group[0], 
        group[1],
        group[2],
        group[3],
        group[4],
        group[5],
        group[6],
        group[7],
        group[8],
        group[9],
        group[10],
        group[11],
        group[12],
        group[13],
        ) for group in op_ex]

    loan_int_rate = [getattr(report, "loan_int_rate") for report in reports]
    loan_term = [getattr(report, "loan_term") for report in reports]

    loan_p_i = list(zip(debt_values, loan_int_rate, loan_term))    
    p_i = [loan_principal_interest(group[0], group[1], group[2]) for group in loan_p_i]

    total_expenses = sum(expenses) + sum(p_i)
    total_cashflow = total_monthly_income - total_expenses

    points = [getattr(report, "points") for report in reports]
    loan_pts = list(zip(purchase_prices, points))
    final_loan_points = [loan_points(group[0], group[1]) for group in loan_pts]


    closing_costs = [getattr(report, "purchase_closing_cost") for report in reports]
    repair_costs = [getattr(report, "est_repair_cost") for report in reports]

    total_cash_invested =  list(zip(down_payments_amounts, closing_costs, repair_costs))
    total_cash = [total_cash_needed(group[0], group[1], group[2]) for group in total_cash_invested]
    total_cash_sum = sum(total_cash)

    coc_roi = cash_on_cash_ROI(total_cashflow, total_cash_sum)

    properties = len(reports)

    context = {
        'reports': reports, 
        'portfolio_value': portfolio_value, 
        'total_equity': total_equity, 
        'total_monthly_income': total_monthly_income,
        'total_expenses': total_expenses,
        'total_cashflow': total_cashflow,
        'properties': properties,
        'coc_roi': coc_roi,
        'debt': debt,
        }
    return render(request, 'calculator/dashboard.html', context)

@method_decorator(login_required, name='dispatch')
class ReportsView(ListView):
    model = RentalPropCalcReport
    template_name = 'calculator/reports.html'
    paginate_by = 5
    context_object_name = 'report_object_list'

    def get_queryset(self):
        return RentalPropCalcReport.objects.filter(owner=self.request.user).order_by('-updated_at')
    
@login_required
def rental_prop_calculator(request):
    """The calculator page"""
    try:
        user_settings = UserSettings.objects.get(user=request.user)
    except:
        user_settings = None
    if request.method != 'POST':
        form = RentalPropForm(instance=user_settings)
    else:
        form = RentalPropForm(request.POST, request.FILES)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.owner = request.user
            new_form.save()
            pk = new_form.pk    
            return redirect(f'/report/{pk}')

    context = {'form': form}
    return render(request, 'calculator/rental_prop_calculator.html', context)

@method_decorator(login_required, name='dispatch')
class Report(ProcessReportMixin, View):
    """The report Page"""
    model = RentalPropCalcReport
    template = 'calculator/report.html'


@login_required
def delete_report(request, pk):
    """Delete report"""
    try:
        report = RentalPropCalcReport.objects.get(id=pk)
    except:
        raise Http404
    if report.owner != request.user:
        raise Http404

    usr_settings = UserSettings.objects.get(user=request.user)

    if getattr(usr_settings, 'blacklist_bool'):
        addr = getattr(report, 'prop_address')
        city = getattr(report, 'prop_city')
        state = getattr(report, 'prop_state')
        zipcode = getattr(report, 'prop_zip')

        current_json = getattr(usr_settings, 'addr_blacklist')

        if not f'{addr} {city}, {state} {zipcode}' in current_json[request.user.username]['addresses']:
            new_json = current_json[request.user.username]['addresses']
            new_json.append(f'{addr} {city}, {state} {zipcode}')
        else: 
            new_json = current_json[request.user.username]['addresses']

        obj, _ = UserSettings.objects.update_or_create(
            user=request.user,
            defaults={'addr_blacklist': {
                    request.user.username: {
                        'addresses': new_json,
                    }
                } 
            }
        )
    
    report.delete()
    return redirect('calculator:reports')

@login_required
def edit_rental_prop_calc(request, pk):
    """Edit a report"""
    try:
        item = RentalPropCalcReport.objects.get(id=pk)
    except:
        raise Http404
    if item.owner != request.user:
        raise Http404
    if request.method == 'POST':
        # POST data submitted; process data.
        
        form = RentalPropForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect(f'/report/{pk}')

    else:
        # Initial request; pre-fill form with the current entry.
        form = RentalPropForm(instance=item)

    # Display a blank or invalid form.
    context = {'item': item,'form': form}
    return render(request, 'calculator/rental_prop_calculator.html', context)

@method_decorator(login_required, name='dispatch')
class ViewReportPDF(CreatePdfMixin, View):
    """Creates PDF of report data"""
    model = RentalPropCalcReport
    template = 'calculator/report_pdf.html'


@login_required
def settings(request):
    """User Settings Page"""
    item, _ = UserSettings.objects.get_or_create(
                user=request.user, 
                defaults={'user': request.user}
                )
    if item.user != request.user:
        raise Http404
    if request.method == 'POST':
        # POST data submitted; process data.
        form = UserSettingsForm(request.POST, instance=item)
        if form.is_valid():
            form.save()
            if request.user.is_superuser:
                clear_crons(request.user)
                make_crons(request.user)
            return redirect('calculator:settings')

    else:
        # Initial request; pre-fill form with the current entry.
        form = UserSettingsForm(instance=item)

    # Display a blank or invalid form.
    context = {'item': item,'form': form}
    return render(request, 'calculator/settings.html', context)
