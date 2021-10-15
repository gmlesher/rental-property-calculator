import dash
from dash import dcc
from dash import dash_table
import plotly.express as px
from django_plotly_dash import DjangoDash
import pandas as pd



app1 = DjangoDash('MonthlyExpenses')
def app1_serve_layout():
    """Returns a pie chart from data in expense_report.csv"""
    
    df = pd.read_csv('expense_report.csv')
    fig = px.pie(df, values='$', names='expense')
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label', 
        hovertemplate="%{label}: %{value:$,.0f}"
        )

    return dcc.Graph(id="expenses-pie-chart", figure=fig)

app2 = DjangoDash('MonthlyIncome')
def app2_serve_layout():
    """Returns a pie chart from data in income_report.csv"""

    df = pd.read_csv('income_report.csv')
    fig = px.pie(df, values='$', names='income')
    fig.update_traces(
        textposition='inside', 
        textinfo='percent+label', 
        hovertemplate="%{label}: %{value:$,.0f}"
        )

    return dcc.Graph(id="income-pie-chart", figure=fig)


app3 = DjangoDash('AOTTable')
def app3_serve_layout():
    """Returns a table of data from aot_report.csv"""

    df = pd.read_csv('aot_report.csv')
    # print(df.columns)
    # print(df.iloc[[3]], df.iloc[[8]])



    table = dash_table.DataTable(
        id='AOT-table',
        fixed_columns={'headers': True, 'data': 1},
        style_table={'minWidth': '100%'},
        columns=[{'name': i, 'id': i} for i in df.columns],
        data=df.to_dict('records'),
        style_as_list_view=True,
        style_cell={
            'padding': '0 15px 0 15px',
            'border': 'none'
            },
        style_cell_conditional=[
            {
                'if': {'column_id': ' '},
                'textAlign': 'left',
                'width': '10%',
            }
        ],
        style_data_conditional=[
            {
                'if': {'row_index': 'odd'},
                'backgroundColor': 'rgb(248, 248, 248)'
            }
        ],
        style_header={
            'backgroundColor': 'rgb(255, 255, 255)',
            'fontWeight': 'bold',
        }
        )

    return table

app4 = DjangoDash('IncExpCashflow')
def app4_serve_layout():
    """Returns a line graph from data in inc_exp_cashflow_report.csv"""

    df = pd.read_csv("inc_exp_cashflow_report.csv")
    fig = px.line(df, 
        x='year', 
        y=['Income', 'Expenses', 'Cashflow'], 
        title="Income, Expenses and Cashflow", 
        )
    fig.update_layout(legend_title_text='', 
        legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
    fig.update_traces(hovertemplate='%{x}: %{y:$,.0f}')
    fig.update_xaxes(showticklabels=False, nticks=15, title='Year')
    fig.update_yaxes(title='$(USD)')

    return dcc.Graph(id="ieo-graph", figure=fig)

app5 = DjangoDash('LoanBalanceValueEquity')
def app5_serve_layout():
    """Returns an area graph from data in loanbal_value_equity_report.csv"""

    df = pd.read_csv('loanbal_value_equity_report.csv')
    fig = px.line(df, 
        x='year', 
        y=['Loan Balance', 'Property Value', 'Equity'], 
        title="Loan Balance, Value and Equity", 
        )
    fig.update_layout(legend_title_text="", 
        legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            )
        )
    fig.update_traces(hovertemplate='%{x}: %{y:$,.0f}')
    fig.update_xaxes(showticklabels=False, nticks=15, title='Year')
    fig.update_yaxes(title='$(USD)')

    return dcc.Graph(id="lbve-graph", figure=fig)

app1.layout = app1_serve_layout
app2.layout = app2_serve_layout
app3.layout = app3_serve_layout
app4.layout = app4_serve_layout
app5.layout = app5_serve_layout