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
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].choices = [[cat.id, f"{cat.type} | {cat.name}"] for cat in Category.objects.all()]

    class Meta:
        model = Operation
        fields = ('amount', 'category', 'date')
        widgets = {
            'amount': forms.TextInput(attrs={"placeholder": "Сумма операции"}),
            'date': forms.DateInput(attrs={"placeholder": "Дата операции"}),
        }
    
    def clean_amount(self):
        amount = self.cleaned_data["amount"]
        if amount <= 0:
            raise ValidationError("Сумма должна быть больше нуля")
        return amount

class ExportDataForm(forms.Form):
    date = forms.ChoiceField(label="Дата", choices=DATE_CHOICES)