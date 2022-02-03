from .models import *
from django import forms
from django.core.exceptions import ValidationError

class OperationForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Категория не выбрана'

    class Meta:
        model = Operation
        fields = ('amount', 'category')
        
        widgets = {
            'amount': forms.TextInput(attrs={"class": "form-control", "placeholder": "Введите сумму затрат"}),
            'category': forms.Select(attrs={"class": "form-control"})
        }
    
    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise ValidationError("Сумма должна быть больше нуля")
        return amount