# 3rd party imports
import pandas as pd
import os

# My file imports
from rentalcalc.settings import BASE_DIR

"""Functions for creating and combining dataframes"""
root_path = BASE_DIR

def create_opex_dataframe(categorys, amounts):
    """creates operating expenses dataframe"""
    df = pd.DataFrame({
        'expense': categorys,
        '$': amounts
        })
    return df.to_csv(os.path.join(root_path, 'expense_report.csv'), index=False)

def create_combine_pi_dataframe(mortgage_pmt):
    """creates principal and insurance dataframe
    and combines it with operating expenses dataframe"""
    df = pd.read_csv(os.path.join(root_path, 'expense_report.csv'))
    df_2 = pd.DataFrame({
        'expense': ['P&I'],
        '$': [round(mortgage_pmt)],
        },
        index=[13])
    return pd.concat([df, df_2]).to_csv(os.path.join(root_path, 'expense_report.csv'))

def create_income_dataframe(income):
    """creates dataframe for all income"""
    df = pd.DataFrame({
        'income': ['Gross Rent', 'Other'],
        '$': income
        })
    return df.to_csv(os.path.join(root_path, 'income_report.csv'), index=True)

def create_aot_dataframe(aot_tuples):
    """creates dataframe for analysis over time"""
    counter = 0
    new_list_of_tuples = []
    for i in aot_tuples:
        counter += 1
        year = f'Year {counter}'
        new_tuple = (year, *i)
        new_list_of_tuples.append(new_tuple)

    df = pd.DataFrame(new_list_of_tuples)
    df[1] = df[1].apply(lambda x: "${:,.0f}".format(x))
    df[2] = df[2].apply(lambda x: "${:,.0f}".format(x))
    df[3] = df[3].apply(lambda x: "${:,.0f}".format(x))
    df[4] = df[4].apply(lambda x: "{:.2f}%".format(x))
    df[5] = df[5].apply(lambda x: "${:,.0f}".format(x))
    df[6] = df[6].apply(lambda x: "${:,.0f}".format(x))
    df[7] = df[7].apply(lambda x: "${:,.0f}".format(x))
    df[8] = df[8].apply(lambda x: "${:,.0f}".format(x))
    df[9] = df[9].apply(lambda x: "{:.2f}%".format(x))
    df = df.set_index(0).T


    def list_length_greater_than_30(n):
        return [0, 4, 9, 14, 19, 29, (n-1)]

    def list_length_less_than_30(n):
        return [0, 1, 4, 9, 14, 19, (n-1)]

    def list_length_less_than_20(n):
        return [0, 1, 2, 4, 9, 14, (n-1)]

    def list_length_less_than_15(n):
        return [0, 1, 2, 3, 4, 9, (n-1)]

    def list_length_less_than_10(n):
        if n == 10 or n == 9:
            return [0, 1, 2, 3, 4, 7, (n-1)]
        elif n == 8:
            return [0, 1, 2, 3, 4, 5, (n-1)]

    def list_length_less_than_7(n):
        return list(range(n))


    if len(df.columns) >= 31:
        df = df.iloc[:, lambda df: list_length_greater_than_30(len(df.columns))]
    elif 20 < len(df.columns) <= 30:
        df = df.iloc[:, lambda df: list_length_less_than_30(len(df.columns))]
    elif 15 < len(df.columns) <= 20:
        df = df.iloc[:, lambda df: list_length_less_than_20(len(df.columns))]
    elif 10 < len(df.columns) <= 15:
        df = df.iloc[:, lambda df: list_length_less_than_15(len(df.columns))]
    elif 7 < len(df.columns) <= 10:
        df = df.iloc[:, lambda df: list_length_less_than_10(len(df.columns))]
    elif len(df.columns) <= 7:
        df = df.iloc[:, lambda df: list_length_less_than_7(len(df.columns))]
    
    cats = [
        'Total Annual Income', 
        'Total Annual Expenses', 
        'Total Annual Cashflow',
        'Cash on Cash ROI',
        'Property Value',
        'Equity',
        'Loan Balance',
        'Total Profit if Sold',
        'Annualized Total Return'
        ]
    df.insert(0, " ", cats, True)
    return df.to_csv(os.path.join(root_path,'aot_report.csv'), index=False)

def create_inc_exp_cashflow_dataframe(iec_tuples):
    """Creates dataframe for income, expenses and cashflow"""
    counter = 0
    new_list_of_tuples = []
    for i in iec_tuples:
        counter += 1
        year = f'Year {counter}'
        new_tuple = (year, *i)
        new_list_of_tuples.append(new_tuple)

    df = pd.DataFrame(new_list_of_tuples, columns=[
                'year', 
                'Income', 
                'Expenses', 
                'Cashflow'
            ])

    return df.to_csv(os.path.join(root_path, 'inc_exp_cashflow_report.csv'), index=True)

def create_loanbalance_value_equity_dataframe(lbve_tuples):
    """Creates dataframe for loan balance, property value and equity"""
    counter = 0
    new_list_of_tuples = []
    for i in lbve_tuples:
        counter += 1
        year = f'Year {counter}'
        new_tuple = (year, *i)
        new_list_of_tuples.append(new_tuple)

    df = pd.DataFrame(new_list_of_tuples, columns=[
                'year', 
                'Loan Balance', 
                'Property Value', 
                'Equity'
            ])

    return df.to_csv(os.path.join(root_path, 'loanbal_value_equity_report.csv'), index=True)