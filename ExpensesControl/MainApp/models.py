from django.contrib.auth.models import User
from django.db import models

class Category(models.Model):
    name = models.CharField(verbose_name="Название", max_length=30)
    
    def __str__(self) -> str:
        return self.name