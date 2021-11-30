from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import Http404
from django.views.generic import ListView

from bot.forms import BotRentalPropForm
from .utils import run_bot_logic
from .models import BotRentalReport
from calculator.calc import *

@login_required
def run_bot(request):
    """Run bot and save model objects of data"""
    run_bot_logic(request.user)
    return redirect('bot:bot-reports')
    

@login_required
def bot_report(request, pk):
    """The bot report page"""
    r = BotRentalReport.objects.get(id=pk)
    if r.owner != request.user:
        raise Http404
        
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
    dwn_pmt_percent = f'{round((dwn_pmt/r.purchase_price) * 100, 2):g}'
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
    return render(request, 'bot/bot_report.html', context)

@method_decorator(login_required, name='dispatch')
class BotReportsView(ListView):
    model = BotRentalReport
    template_name = 'bot/bot_reports.html'
    paginate_by = 5
    context_object_name = 'bot_object_list'

    def get_queryset(self):
        return BotRentalReport.objects.filter(owner=self.request.user).order_by('-updated_at')

@login_required
def bot_delete_report(request, pk):
    """Delete report"""
    try:
        report = BotRentalReport.objects.get(id=pk)
    except:
        raise Http404
    if report.owner != request.user:
        raise Http404
    report.delete()
    return redirect('bot:bot-reports')

@login_required
def bot_edit_rental_prop_calc(request, pk):
    """Edit a report"""
    try:
        item = BotRentalReport.objects.get(id=pk)
    except:
        raise Http404
    if item.owner != request.user:
        raise Http404
    if request.method == 'POST':
        # Initial request; pre-fill form with the current entry.
        form = BotRentalPropForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            return redirect(f'/bot/bot-report/{pk}')

    else:
        # POST data submitted; process data.
        form = BotRentalPropForm(instance=item)

    # Display a blank or invalid form.
    context = {'item': item,'form': form}
    return render(request, 'bot/bot_calculator.html', context)