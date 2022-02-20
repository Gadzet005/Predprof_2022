import pandas as pd
from sklearn.linear_model import LinearRegression
from urllib.request import urlopen
from bs4 import BeautifulSoup
import ssl
import json

from .models import *
from MainApp.models import Variable

class ExpenseForecast:
    def __init__(self) -> None:
        self.monthlyIncomes = list()
        self.monthlyExpenses = list()
        self.model = LinearRegression()

    def addMonth(self, monthlyIncome, monthlyExpense) -> None:
        self.monthlyIncomes.append(monthlyIncome)
        self.monthlyExpenses.append(monthlyExpense)
        self.model.fit(pd.DataFrame(self.monthlyIncomes), pd.DataFrame(self.monthlyExpenses))

    def getForecast(self, currentMonthIncome) -> int:
        try:
            return int(self.model.coef_ * currentMonthIncome)
        except:
            return 0

    def get_sum(self, operations):
        income, expense = 0, 0
        for operation in operations:
            if operation.category.type == "Расход":
                expense += operation.amount
            else:
                income += operation.amount
        return income, expense

    def createForecast(self, operations):
        month_list = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", 
                      "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
        month_data = {}
        today = date.today()
        current_month, current_year, last_year = today.month, today.year, today.year - 1

        # Добавляем точки в модель зависимости расходов от доходов. Точка соответствует месяцу.
        for month in range(1, 13):
            if month != current_month:
                if month > current_month:
                    year = last_year
                else:
                    year = current_year
                
                operations_in_month = operations.filter(date__year=year, date__month=month)
                income, expense = self.get_sum(operations_in_month)
                month_data[year, month] = (income, expense)
                self.addMonth(income, expense)
        
        cur_income, cur_expense = self.get_sum(operations.filter(date__year=current_year, date__month=current_month))
        forecast_expense = self.getForecast(cur_income) + cur_expense

        # Формируем список расходов и доходов по месяцам
        month_data[current_year, current_month] = (cur_income, cur_expense)
        sorted_keys = sorted(month_data, key=lambda x: (x[0], x[1]), reverse=True)
        sorted_data = {month_list[key[1] - 1] + " " + str(key[0]): month_data[key] for key in sorted_keys[:6]}

        return forecast_expense, sorted_data

class CPI:
    def __init__(self):
        cpi, result = Variable.objects.get_or_create(name="ИПЦ")
        if result:
            CPI.updateCPI()

        self.cpi_data = json.loads(cpi.value)

    def getNextTreeMonth(self, value):
        return round(value * sum(self.cpi_data[:3]) / 300)

    def getNextSixMonth(self, value):
        return round(value * sum(self.cpi_data[:6]) / 600)

    def getNextYear(self, value):
        return round(value * sum(self.cpi_data) / 1200)
    
    @staticmethod
    def updateCPI():
        try:
            url = "https://www.statbureau.org/ru/russia/cpi"
            gcontext = ssl.SSLContext(ssl.PROTOCOL_TLSv1)
            html = urlopen(url, context=gcontext).read()
            soup = BeautifulSoup(html, features="html.parser")
            for script in soup(["script", "style"]):
                script.extract()
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            arr = text.split("\n")
            arrcpi = list()
            for i in range(72, 91):
                if "," in arr[i]:
                    arrcpi.append(float(arr[i].replace(",", ".")))
                if len(arrcpi) == 12:
                    break
            cpi = arrcpi
        except:
            cpi = [100 for i in range(12)]
        finally:
            db_cpi, result = Variable.objects.get_or_create(name="ИПЦ")
            db_cpi.value = json.dumps(cpi)
            db_cpi.save()
            return db_cpi