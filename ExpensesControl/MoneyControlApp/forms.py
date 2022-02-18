from .models import *
from MainApp.models import *
from django import forms
from django.core.exceptions import ValidationError
from datetime import date, timedelta

def get_initial_export_date():
    return date.today() - timedelta(days=30)

class OperationForm(forms.ModelForm):
    type = forms.ChoiceField(label="Тип", choices=(["Расход", "Расход"], ["Доход", "Доход"]),
                             widget=forms.Select(attrs={"id": "id_type"}))
    date = forms.DateField(label="Дата", initial=date.today, widget=forms.TextInput(attrs={"type": "date"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Не выбрана"

    class Meta:
        model = Operation
        fields = ('name', 'type', 'category', 'amount', 'date')
        widgets = {
            'name': forms.TextInput(attrs={"placeholder": "Например: поход в кино"}),
            'amount': forms.NumberInput(attrs={"placeholder": "Сумма операции"}),
            'category': forms.Select(attrs={"id": "id_category"}),
        }
    
    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise ValidationError("Сумма должна быть больше нуля")
        return amount

class ExportDataForm(forms.Form):
    date_begin = forms.DateField(label="Начало периода", initial=get_initial_export_date,
                                 widget=forms.TextInput(attrs={"type": "date"}))
    date_end = forms.DateField(label="Конец периода", initial=date.today, 
                               widget=forms.TextInput(attrs={"type": "date"}))