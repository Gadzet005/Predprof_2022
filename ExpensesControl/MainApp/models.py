from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(verbose_name="Название", max_length=30, unique=True)
    type = models.CharField(verbose_name="Тип", max_length=30)
    
    def __str__(self):
        return self.name
    
class Variable(models.Model):
    name = models.CharField(verbose_name="Название", max_length=30, unique=True)
    value = models.CharField(verbose_name="Значение", max_length=100)

    def __str__(self):
        return self.name