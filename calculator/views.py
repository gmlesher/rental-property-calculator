from django.shortcuts import render, redirect

# My files
from .models import RentalPropCalcReport
from .forms import RentalPropForm
from .calc import *
from . import plotly_app

def index(request):
    """The home page for the Rental Property Calculator."""
<<<<<<< Updated upstream
    reports = RentalPropCalcReport.objects.all().order_by('-updated_at')
    context = {'reports': reports}
    return render(request, 'calculator/index.html', context)
=======
    return render(request, 'calculator/index.html')

@login_required
def dashboard(request):
    """The dashboard page for a user"""
    reports = RentalPropCalcReport.objects.filter(owner=request.user)
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

@login_required
def reports(request):
    """The reports page for a user"""
    reports = RentalPropCalcReport.objects.filter(owner=request.user).order_by('-updated_at')
    context = {'reports': reports}
    return render(request, 'calculator/reports.html', context)
>>>>>>> Stashed changes
    

def rental_prop_calculator(request):
    """The calculator page"""
    form = RentalPropForm(request.POST, request.FILES or None)
    if form.is_valid():
        new_form = form.save()
        pk = new_form.pk
        return redirect(f'/report/{pk}')

    context = {'form': form}
    return render(request, 'calculator/rental_prop_calculator.html', context)


def report(request, pk):
    """The report page"""
    r = RentalPropCalcReport.objects.get(id=pk)
<<<<<<< Updated upstream
    if r.after_repair_value == None:
        r.after_repair_value = r.purchase_price
=======
    if r.owner != request.user:
        raise Http404
>>>>>>> Stashed changes
    mo_income = monthly_income(r.gross_monthly_rent, r.other_monthly_income)
    total_op_exp = total_operating_expenses(
        mo_income, 
        r.electricity,
        r.gas,
        r.water_sewer,
        r.pmi,
        r.garbage,
        r.hoa,
        r.monthly_insurance,
        r.prop_annual_taxes,
        r.other_monthly_expenses,
        r.vacancy,
        r.repairs_maint,
        r.cap_expenditures,
        r.mgmt_fees
        )
    dwn_pmt = down_payment(r.purchase_price, r.down_payment, r.down_payment_2)
    loan_amt = loan_amount(r.purchase_price, dwn_pmt)
    loan_pts = loan_points(r.purchase_price, r.points)
    ttl_clos_costs = total_closing_costs(r.purchase_closing_cost, loan_pts)
    p_i = loan_principal_interest(loan_amt, r.loan_int_rate, r.loan_term)
    total_cash = total_cash_needed(dwn_pmt, ttl_clos_costs, r.est_repair_cost)
    mo_exp = monthly_expenses(total_op_exp, p_i)
    cashflow = monthly_cashflow(mo_income, mo_exp)
    n_o_i = noi(mo_income, total_op_exp)
    purchase_cap_rt = purchase_cap(n_o_i, r.purchase_price)
    pro_forma_cap_rt = pro_forma_cap(n_o_i, r.after_repair_value)
    coc_roi = cash_on_cash_ROI(cashflow, total_cash)
    total_cost = total_project_cost(r.purchase_price, ttl_clos_costs, r.est_repair_cost)
    aot = analysis_over_time(r.annual_income_growth, r.annual_pv_growth, r.annual_expenses_growth, r.sales_expenses, r.loan_term, loan_amt, r.loan_int_rate, mo_income, total_op_exp, p_i, total_cash, r.after_repair_value)

    two_pct_rule = two_percent_rule(total_cost, mo_income)
    total_init_equity = total_initial_equity(r.after_repair_value, r.purchase_price, dwn_pmt)
    grm = gross_rent_multiplier(mo_income, r.purchase_price)
    debt_cov_rto = debt_coverage_ratio(n_o_i, p_i)

    context = {
        'r': r, 
        'mo_income': mo_income,
        'total_op_exp': total_op_exp,
        'dwn_pmt': dwn_pmt,
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
    return render(request, 'calculator/report.html', context)

def delete_report(request, pk):
    """Delete report"""
    try:
        report = RentalPropCalcReport.objects.get(id=pk)
    except:
        raise Http404
    RentalPropCalcReport.objects.filter(id=pk).delete()
    return redirect('calculator:index')


def edit_rental_prop_calc(request, pk):
    """Edit a report"""
    try:
        item = RentalPropCalcReport.objects.get(id=pk)
    except:
        raise Http404
    if request.method == 'POST':
        # Initial request; pre-fill form with the current entry.
        form = RentalPropForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect(f'/report/{pk}')

    else:
        # POST data submitted; process data.
        form = RentalPropForm(instance=item)

    # Display a blank or invalid form.
    context = {'item': item,'form': form}
    return render(request, 'calculator/rental_prop_calculator.html', context)