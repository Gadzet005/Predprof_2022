from django.db import models
from django.contrib.auth.models import User
from MainApp.models import Category
from datetime import date

class Operation(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name="Сумма")
    date = models.DateField(verbose_name="Дата", default=date.today)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.user}: {self.amount}"