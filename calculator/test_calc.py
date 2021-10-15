from django.test import TestCase
from calculator import calc

class TestCalc(TestCase):
    def test_monthly_income(self):
        self.assertEqual(calc.monthly_income(1200, 200), 1400)

    def test_total_operating_expenses(self):
        self.assertEqual(calc.total_operating_expenses(1200, 10, 20, 30, 100, \
            70, 200, 300, 200, 25, 2, 2, 2, 10), 963)

    def test_down_payment(self):
        self.assertEqual(calc.down_payment(100000, None, None), 0)
        self.assertEqual(calc.down_payment(100000, 25, None), 25000)
        self.assertEqual(calc.down_payment(100000, None, 46750), 46750)
        self.assertEqual(calc.down_payment(100000, None, 0), 0)
        self.assertEqual(calc.down_payment(100000, None, 1), 1)

    def test_loan_amount(self):
        self.assertEqual(calc.loan_amount(230000, 46000), 184000)
        self.assertEqual(calc.loan_amount(200000, 200000), 0)
        self.assertEqual(calc.loan_amount(200000, 200001), 0)

    def test_loan_points(self):
        self.assertEqual(calc.loan_points(230000, 3), 6900)
        self.assertEqual(calc.loan_points(200000, 1), 2000)
        self.assertEqual(calc.loan_points(200000, 0), 0)
        self.assertEqual(calc.loan_points(200000, None), 0)

    def test_total_closing_costs(self):
        self.assertEqual(calc.total_closing_costs(4000, 1000), 5000)
        self.assertEqual(calc.total_closing_costs(3450, 1750), 5200)
        self.assertEqual(calc.total_closing_costs(6000, 0), 6000)
        self.assertEqual(calc.total_closing_costs(1734, None), 1734)  
        self.assertEqual(calc.total_closing_costs(None, None), 0)

    def test_loan_principal_interest(self):
        self.assertEqual(calc.loan_principal_interest(100000, 3.4, 15), 710)
        self.assertEqual(calc.loan_principal_interest(220000, 15.5, 30), 2870)
        self.assertEqual(calc.loan_principal_interest(10000, 1.2, 30), 33)

    def test_total_cash_needed(self):
        self.assertEqual(calc.total_cash_needed(50000, 6000, 4000), 60000)
        self.assertEqual(calc.total_cash_needed(50000, 6000, None), 56000)
        self.assertEqual(calc.total_cash_needed(50000, 0, None), 50000)
        self.assertEqual(calc.total_cash_needed(32489, 1, 1), 32491)

    def test_monthly_cashflow(self):
        self.assertEqual(calc.monthly_cashflow(1200, 1100), 100)
        self.assertEqual(calc.monthly_cashflow(1000, 1200), -200)

    def test_noi(self):
        self.assertEqual(calc.noi(1200, 1100), 1200)
        self.assertEqual(calc.noi(2900, 2580), 3840)
        self.assertEqual(calc.noi(2900, 0), 34800)
        self.assertEqual(calc.noi(2900, None), 34800)

    def test_purchase_cap(self):
        self.assertEqual(calc.purchase_cap(13368, 200000), 6.68)
        self.assertEqual(calc.purchase_cap(16000, 450000), 3.56)
        self.assertEqual(calc.purchase_cap(0, 0,), 0)
        self.assertEqual(calc.purchase_cap(0, 200000), 0)

    def test_pro_forma_cap(self):
        self.assertEqual(calc.pro_forma_cap(16000, 280000), 5.71)
        self.assertEqual(calc.pro_forma_cap(16000, 0), 0)
        self.assertEqual(calc.pro_forma_cap(0, 280000), 0)
        self.assertEqual(calc.pro_forma_cap(11567, 231700), 4.99)

    def test_cash_on_cash_ROI(self):
        self.assertEqual(calc.cash_on_cash_ROI(367, 48000), 9.18)
        self.assertEqual(calc.cash_on_cash_ROI(400, 48000), 10)
        self.assertEqual(calc.cash_on_cash_ROI(-250, 38921), -7.71)

    def test_total_project_cost(self):
        self.assertEqual(calc.total_project_cost(120000, 5000, 12000), 137000)
        self.assertEqual(calc.total_project_cost(120000, None, None), 120000)
        self.assertEqual(calc.total_project_cost(120000, 1200, None), 121200)
        self.assertEqual(calc.total_project_cost(120000, None, 1200), 121200)

    def test_aot_annual_income(self):
        self.assertEqual(calc.aot_annual_income(2, 2500, 30), [30000, 30600, 31212, 31836, 32473, 33122, 33785, 34461, 35150, 35853, 36570, 37301, 38047, 38808, 39584, 40376, 41184, 42007, 42847, 43704, 44578, 45470, 46379, 47307, 48253, 49218, 50203, 51207, 52231, 53275])
        self.assertEqual(calc.aot_annual_income(None, 2500, 30), [30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000, 30000])
        self.assertEqual(calc.aot_annual_income(2, None, 30), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(calc.aot_annual_income(2, 2500, None), [])
        self.assertEqual(calc.aot_annual_income(None, None, None), [])
    def test_aot_annual_expenses(self):
        self.assertEqual(calc.aot_annual_expenses(2, 1500, 850, 15), [28200, 28560, 28927, 29302, 29684, 30073, 30471, 30876, 31290, 31712, 32142, 32581, 33028, 33485, 33951])
        self.assertEqual(calc.aot_annual_expenses(None, 1500, 850, 15), [28200, 28200, 28200, 28200, 28200, 28200, 28200, 28200, 28200, 28200, 28200, 28200, 28200, 28200, 28200])
        self.assertEqual(calc.aot_annual_expenses(2, 1200, None, 15), [14400, 14688, 14982, 15281, 15587, 15899, 16217, 16541, 16872, 17209, 17554, 17905, 18263, 18628, 19000])
        self.assertEqual(calc.aot_annual_expenses(2, 0, None, 15), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(calc.aot_annual_expenses(2, 1500, 800, None), [])

    def test_aot_annual_cashflow(self):
        self.assertEqual(calc.aot_annual_cashflow([1200, 1500], [1000, 1200]), [200, 300])
        self.assertEqual(calc.aot_annual_cashflow([0, 0], [1000, 1200]), [-1000, -1200])
        self.assertEqual(calc.aot_annual_cashflow([0, 0], [0, 0]), [0, 0])
        self.assertEqual(calc.aot_annual_cashflow(None, None), [0])

    def test_aot_cash_on_cash_ROI(self):
        self.assertEqual(calc.aot_cash_on_cash_ROI([10500, 10600], 48000), [21.88, 22.08])
        self.assertEqual(calc.aot_cash_on_cash_ROI(None, 48000), [])

    def test_aot_property_value(self):
        self.assertEqual(calc.aot_property_value(2, 280000, 30), [285600, 291312, 297138, 303081, 309143, 315325, 321632, 328065, 334626, 341318, 348145, 355108, 362210, 369454, 376843, 384380, 392068, 399909, 407907, 416065, 424387, 432874, 441532, 450362, 459370, 468557, 477928, 487487, 497237, 507181])
        self.assertEqual(calc.aot_property_value(None, 280000, 5), [280000, 280000, 280000, 280000, 280000])
        self.assertEqual(calc.aot_property_value(2, None, 5), [0, 0, 0, 0, 0])
        self.assertEqual(calc.aot_property_value(2, 150000, None), [])

    def test_aot_loan_balance(self):
        self.assertEqual(calc.aot_loan_balance(1200, 160000, 15, 4.5), [152650, 144962, 136920, 128510, 119713, 110512, 100888, 90822, 80293, 69281, 57763, 45716, 33116, 19936, 6151])
        self.assertEqual(calc.aot_loan_balance(1200, 160000, 0, 4.5), [])
        self.assertEqual(calc.aot_loan_balance(1200, 0, 15, 4.5), [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0])
        self.assertEqual(calc.aot_loan_balance(1200, 120000, 15, 0), [105600, 91200, 76800, 62400, 48000, 33600, 19200, 4800, 0, 0, 0, 0, 0, 0, 0])

    def test_aot_equity(self):
        self.assertEqual(calc.aot_equity([280000, 286000], [160000, 155000]), [120000, 131000])

    def test_aot_total_profit_if_sold(self):
        self.assertEqual(calc.aot_total_profit_if_sold([180000, 190000], [100000, 99000], [5600, 5700], 9, 48000), [21400, 37200])
        self.assertEqual(calc.aot_total_profit_if_sold([180000, 190000], [100000, 99000], [5600, 5700], None, None), [85600, 102300])

    def test_aot_annualized_total_return(self):
        self.assertEqual(calc.aot_annualized_total_return([85600, 102300], 48000), [178.33, 76.95])
        self.assertEqual(calc.aot_annualized_total_return([85600, 102300], None), [0, 0])