from django.db import models
from django.contrib.auth.models import User
from MainApp.models import Category
from datetime import date

class Operation(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    name = models.CharField(verbose_name="Название", max_length=50, default="Операция")
    amount = models.IntegerField(verbose_name="Сумма")
    date = models.DateField(verbose_name="Дата", default=date.today)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f"{self.user}: {self.amount}"
    
    @staticmethod
    def get_sum(operations):
        op_sum = 0
        for operation in operations:
            if operation.category.type == "Расход":
                op_sum -= operation.amount
            else:
                op_sum += operation.amount
        return op_sum