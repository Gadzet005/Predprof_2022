from django.db import models
from django.contrib.auth.models import User
from MainApp.models import Category

class Operation(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name="Сумма")
    datetime = models.DateTimeField(verbose_name="Дата и время", auto_now_add=True)
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.user}: {self.amount}"

# Every month balance change
class Operation_EM(models.Model):
    user = models.ForeignKey(User, verbose_name="Пользователь", on_delete=models.CASCADE)
    amount = models.IntegerField(verbose_name="Сумма")
    category = models.ForeignKey(Category, verbose_name="Категория", on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return f"{self.user}: {self.amount}"