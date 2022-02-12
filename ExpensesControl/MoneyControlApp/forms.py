from .models import *
from MainApp.models import *
from django import forms
from django.core.exceptions import ValidationError

DATE_CHOICES = (
('Все время', 'Все время'), 
('День', 'Сегодня'),
('Неделя', 'Неделя'),
('Месяц', 'Месяц'),
('Год', 'Год'),
)

class OperationForm(forms.ModelForm):
    type = forms.ChoiceField(label="Тип", choices=(["Расход", "Расход"], ["Доход", "Доход"]),
                             widget=forms.Select(attrs={"id": "type_select"}))

    class Meta:
        model = Operation
        fields = ('type', 'category', 'amount', 'date')
        widgets = {
            'amount': forms.TextInput(attrs={"placeholder": "Сумма операции"}),
            'date': forms.DateInput(attrs={"placeholder": "Дата операции"}),
            'category': forms.Select(attrs={"id": "cat_select"}),
        }
    
    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise ValidationError("Сумма должна быть больше нуля")
        return amount

class ExportDataForm(forms.Form):
    date = forms.ChoiceField(label="Дата", choices=DATE_CHOICES)