from .dataframes import *

"""Basic Calculations Section"""

def monthly_income(gross_rent, other_income):
    """Returns sum of all property income"""
    income = [gross_rent, other_income]
    rounded_income = [round(i) if i else 0 for i in income]
    create_income_dataframe(rounded_income)
    return round(sum([i if i != None else 0 for i in income]))

def total_operating_expenses(monthly_income, elec, gas, water_sewer, pmi, \
    garbage, hoa, ins, tax, other, vacancy, repairs, cap_ex, mgmt_fees):
    """Returns sum of all operating expenses.
    Operating expenses = sum of all expenses except mortgage payments"""
    tax = int(tax/12)
    if vacancy:
        vac = monthly_income * (vacancy/100) 
    else:
        vac = 0

    if repairs:
        rep = monthly_income * (repairs/100)
    else:
        rep = 0

    if cap_ex:
        cap = monthly_income * (cap_ex/100)
    else:
        cap = 0

    if mgmt_fees:
        mgmt = monthly_income * (mgmt_fees/100)
    else:
        mgmt = 0

    expense_amounts = [elec, gas, water_sewer, pmi, garbage, hoa, \
                        ins, tax, other, vac, rep, cap, mgmt]
    names = ["Electricity", "Gas", "Water/Sewer", "PMI", "Garbage", "HOA", \
                "Insurance", "Tax", "Other", "Vacancy", \
                "Repairs/Maint.", "CapEx", "Mgmt Fees"]
    cleaned_expenses = [None if e == None else round(e) for e in expense_amounts]
    create_opex_dataframe(names, cleaned_expenses)
    return round(sum([i if i != None else 0 for i in cleaned_expenses]))

def down_payment(purchase_price, down_payment, down_payment_2):
    """Returns $ amount of down payment"""
    if down_payment:
        """down payment comes in as a string percentage, possibly with decimal"""
        if type(down_payment) == str:
            down_payment = float(down_payment.strip('%'))
        return round(purchase_price * (down_payment/100))
    elif down_payment_2:
        return down_payment_2
    else:
        return 0

def loan_amount(purchase_price, down_payment):
    """Returns loan amount"""
    if purchase_price > down_payment:
        return purchase_price - down_payment
    else:
        return 0

def loan_points(purchase_price, points):
    """Returns $ amount of loan points"""
    if points:
        return round(purchase_price * (points/100))
    return 0

def total_closing_costs(purchase_closing_cost, loan_pts):
    """Closing costs + loan points if entered"""
    total_cc = [purchase_closing_cost, loan_pts]
    return round(sum([i if i != None else 0 for i in total_cc]))

def loan_principal_interest(loan_amount, loan_int_rate, loan_term):
    """Returns sum of monthly mortgage expenses.
    Formula for monthly loan payments: M = P[i(1+i)^n]/[(1+i)^n-1]"""
    try:
        monthly_rate = (loan_int_rate/100)/12
        months_to_repay = loan_term * 12
        mortgage_pmt = (loan_amount * 
            (monthly_rate * (1 + monthly_rate)**months_to_repay)/ 
            ((1 + monthly_rate)**months_to_repay - 1)
            )
        create_combine_pi_dataframe(mortgage_pmt)
        
        return round(mortgage_pmt)
    except (ZeroDivisionError, Exception):
        create_combine_pi_dataframe(0)
        return 0

def total_cash_needed(down_payment, purchase_closing_cost, est_repair_cost):
    """Returns the total cash needed to cover down payment, closing costs, and
    repairs for project"""
    cash = [down_payment, purchase_closing_cost, est_repair_cost]
    return round(sum([i if i != None else 0 for i in cash]))

def monthly_expenses(op_expenses, p_i):
    """Returns sum of all expenses.
    Monthly expenses = sum of operating expenses + mortgage expenses"""
    return op_expenses + p_i

def monthly_cashflow(monthly_income, monthly_expenses):
    """Returns property cashflow. Cashflow = income - expenses"""
    return monthly_income - monthly_expenses

def noi(monthly_income, total_op_exp):
    """Returns the Net Operating Income of the property evaluated on an 
    annual basis.
    NOI = gross monthly income * 12 - total operating expenses * 12"""
    if monthly_income:
        annual_income = monthly_income * 12
    else:
        annual_income = 0
        
    if total_op_exp:
        annual_op_exp = total_op_exp * 12
    else:
        annual_op_exp = 0
        
    return annual_income - annual_op_exp

def purchase_cap(noi, purchase_price):
    """Returns purchase cap rate.
    Purchase cap rate = net operating income (NOI)/ Purchase Price"""
    try:
        return round((noi/purchase_price) * 100, 2)
    except ZeroDivisionError:
        return 0

def pro_forma_cap(noi, arv):
    """Returns pro forma cap rate.
    Pro forma cap rate = 
    net operating income (NOI)/ After Repair Value.

    *Considers the repairs done on the unit and how much those 
    repairs increased the value of unit
    """
    try:    
        return round((noi/arv) * 100, 2)
    except ZeroDivisionError:
        return 0

def cash_on_cash_ROI(cashflow, total_cash):
    """Returns COCROI as a percentage.
    COCROI formula: annual before tax cash flow/total cash invested"""
    annual_cashflow = cashflow * 12
    try:
        return round((annual_cashflow/total_cash) * 100, 2)
    except ZeroDivisionError:
        return 0
        
def total_project_cost(purchase_price, purchase_closing_cost, est_repair_cost):
    """Returns total property cost. 
    Total project cost = purchase price + closing costs + repair costs"""
    costs = [purchase_price, purchase_closing_cost, est_repair_cost]
    return round(sum([i if i != None else 0 for i in costs]))

"""Financial Info Section"""

def two_percent_rule(total_project_cost, monthly_income):
    """Calculates the % of gross rent to total investment cost"""
    try:
        return monthly_income/total_project_cost * 100
    except ZeroDivisionError:
        return 0

def total_initial_equity(after_repair_value, purchase_price, dwn_pmt):
    """Calculates the total initial equity when purchasing property"""
    return (after_repair_value-purchase_price) + dwn_pmt

def gross_rent_multiplier(monthly_income, purchase_price):
    """Calculates GRM. GRM used to compare against other similar properties in 
    the same market. Lower GRM is better."""
    try:
        return purchase_price/(monthly_income * 12)
    except ZeroDivisionError:
        return 0 

def debt_coverage_ratio(noi, p_i):
    """Calculates the debt coverage ratio, which is used to determine ability to
    generate enough income to cover debt expenses. DCR < 1 means debt 
    expenses not able to be covered by operating income."""
    try:
        return noi/(p_i*12) 
    except ZeroDivisionError:
        return 0

"""Analysis Over Time Section"""

def analysis_over_time(annual_income_growth, annual_pv_growth, annual_expenses_growth, sales_expenses, loan_term, loan_amount, int_rate, monthly_income, operating_expenses, p_i, total_cash, after_repair_value):
    """Returns data in lists for each year the length of the loan term. To be used in dataframe for graphs"""
    total_i = aot_annual_income(annual_income_growth, monthly_income, loan_term)
    total_e = aot_annual_expenses(annual_expenses_growth, operating_expenses, p_i, loan_term)
    total_cashflow = aot_annual_cashflow(total_i, total_e)
    total_coc_roi = aot_cash_on_cash_ROI(total_cashflow, total_cash)
    total_pv = aot_property_value(annual_pv_growth, after_repair_value, loan_term)
    total_loan_balance = aot_loan_balance(p_i, loan_amount, loan_term, int_rate)
    total_equity = aot_equity(total_pv, total_loan_balance)
    total_profit_if_sold = aot_total_profit_if_sold(total_pv, total_loan_balance, total_cashflow,sales_expenses, total_cash)
    total_annual_return = aot_annualized_total_return(total_profit_if_sold, total_cash)
    aot_tuples = list(zip(total_i, total_e, total_cashflow, total_coc_roi, total_pv, total_equity, total_loan_balance, total_profit_if_sold, total_annual_return))
    create_aot_dataframe(aot_tuples)
    iec_tuples = list(zip(total_i, total_e, total_cashflow))
    create_inc_exp_cashflow_dataframe(iec_tuples)
    lbve_tuples = list(zip(total_loan_balance, total_pv, total_equity))
    create_loanbalance_value_equity_dataframe(lbve_tuples)
    return 

def aot_annual_income(annual_income_growth, monthly_income, loan_term):
    """returns a list fo the annual income over the length of the loan term"""
    if annual_income_growth == None:
        annual_income_growth = 0
    if monthly_income == None:
        monthly_income = 0
    if loan_term == None:
        loan_term = 0

    aot_annual_income = []
    current_year_income = 0
    if loan_term == 0:
        aot_annual_income.append(round(monthly_income * 12))
    for year in range(loan_term):
        if year == 0:
            annual_income = monthly_income * 12
            current_year_income += annual_income
            aot_annual_income.append(round(annual_income))
        else:
            current_year_income += (annual_income_growth/100) * current_year_income
            aot_annual_income.append(round(current_year_income))
    return aot_annual_income

def aot_annual_expenses(annual_expenses_growth, operating_expenses, p_i, loan_term):
    """returns a list of the annual expenses over the length of the loan term"""
    if annual_expenses_growth == None:
        annual_expenses_growth = 0
    if p_i == None:
        p_i = 0
    if loan_term == None:
        loan_term = 0

    aot_annual_expenses = []
    annual_operating_expenses = 0
    annual_pi = p_i * 12
    if loan_term == 0 or p_i == 0:
        aot_annual_expenses.append(round(operating_expenses * 12))
    for year in range(loan_term):
        if year == 0:
            annual_operating_expenses = (operating_expenses * 12)
            op_and_p_i = annual_operating_expenses + annual_pi
            aot_annual_expenses.append(round(op_and_p_i))
        else:
            annual_operating_expenses += (annual_expenses_growth/100) * annual_operating_expenses
            op_and_p_i = annual_operating_expenses + annual_pi
            aot_annual_expenses.append(round(op_and_p_i))
    return aot_annual_expenses

def aot_annual_cashflow(total_annual_income, total_annual_expenses):
    """returns a list of the annual cashflow over the length of the loan term"""
    if total_annual_income == None:
        total_annual_income = [0]
    if total_annual_expenses == None:
        total_annual_expenses = [0]

    aot_annual_cashflow = []
    zip_object = zip(total_annual_income, total_annual_expenses)
    for list1, list2 in zip_object:
        aot_annual_cashflow.append(list1-list2)

    return aot_annual_cashflow

def aot_cash_on_cash_ROI(total_annual_cashflow, total_cash):
    """returns a list of the COCROI over the length of the loan term"""
    aot_cash_on_cash_ROI = []
    if total_annual_cashflow == None:
        total_annual_cashflow = []
    else:
        for n in total_annual_cashflow:
            try:
                coc_roi = round((n/total_cash) * 100, 2)
                aot_cash_on_cash_ROI.append(coc_roi)
            except ZeroDivisionError:
                aot_cash_on_cash_ROI.append(0)
    return aot_cash_on_cash_ROI

def aot_property_value(annual_pv_growth, after_repair_value, loan_term):
    """returns a list of property values over the length of the loan term"""
    if annual_pv_growth == None:
        annual_pv_growth = 0
    if after_repair_value == None:
        after_repair_value = 0
    if loan_term == None:
        loan_term = 0

    aot_property_value = []
    current_year_pv = after_repair_value
    if loan_term == 0:
        current_year_pv += (annual_pv_growth/100) * current_year_pv
        aot_property_value.append(round(current_year_pv))
    for year in range(loan_term):
        current_year_pv += (annual_pv_growth/100) * current_year_pv
        aot_property_value.append(round(current_year_pv))
    return aot_property_value

def aot_loan_balance(p_i, loan_amount, loan_term, int_rate):
    """returns the loan balance over loan term on an annual basis.
    calculated by adding monthly principal payments over 1 year.
    principal pmt = total monthly payment - (loan balance * (interest rate/12))"""
    monthly_balances = []
    annual_balances = []
    balance = loan_amount
    if loan_term == 0:
        annual_balances.append(0)
    for month in range(loan_term*12):
        principal = p_i - (balance * ((int_rate/100)/12))
        balance -= principal
        monthly_balances.append(round(balance))

    for monthly_amount in monthly_balances[11::12]:
        if monthly_amount <= p_i:
            monthly_amount = 0
            annual_balances.append(monthly_amount)
        else:
            annual_balances.append(monthly_amount)
    return annual_balances

def aot_equity(property_value, loan_balance):
    """calculates the annual equity"""
    aot_equity = []
    zip_object = zip(property_value, loan_balance)
    for list1, list2 in zip_object:
        aot_equity.append(list1-list2)
    return aot_equity

def aot_total_profit_if_sold(property_value, loan_balance, cashflow, sales_expenses, total_cash):
    """calculates the total profit if a property is sold.
    Property value - (property value * (sales expenses/100)) - loan balance - total cash + cumulative annual cashflow"""
    if sales_expenses == None:
        sales_expenses = 0
    if total_cash == None:
        total_cash = 0
    aot_total_profit_if_sold = []
    cumulative_cashflow_sum = [sum(cashflow[0:i[0]+1]) for i in enumerate(cashflow)]
    zip_object = zip(property_value, loan_balance, cumulative_cashflow_sum)

    for list1, list2, list3 in zip_object:
        sales_exp = list1 * (sales_expenses/100)
        profit = (list1 - sales_exp - list2 - total_cash) + list3
        aot_total_profit_if_sold.append(round(profit))

    return aot_total_profit_if_sold

def aot_annualized_total_return(total_profit_if_sold, total_cash):
    """(total profit if sold/total cash)/years property is held"""
    if total_cash == None:
        total_cash = 0
    aot_annualized_total_return = []

    for count, profit in enumerate(total_profit_if_sold):
        try:
            ann_return = ((1+(profit/total_cash))**(1/(count+1))-1) * 100
            aot_annualized_total_return.append(round(ann_return, 2))
        except ZeroDivisionError:
            aot_annualized_total_return.append(0)

    return aot_annualized_total_return 


# debt_coverage_ratio(-2600, 210000)
# gross_rent_multiplier(2600, 210000)
# total_initial_equity(0, 210000, 0)
# two_percent_rule(216000, 2600)

# aot_annualized_total_return([85600, 102300], None)
# aot_total_profit_if_sold([180000, 190000], [100000, 99000], [5600, 5700], None, None)
# aot_equity([0, 0], [160000, 155000])
# aot_loan_balance(1200, 120000, 15, 0)
# aot_property_value(2, 150000, None)
# aot_cash_on_cash_ROI([12400, 15000], 48000)
# aot_annual_cashflow(None, None)
# aot_annual_expenses(2, 1500, 800, None)
# pro_forma_cap(11567, 231700)
# aot_annual_income(None, None, None)

# analysis_over_time(2, 2, 2, 9, 30, 168000, 4.5, 2600, 1250, 851.23, 48000, 280000)