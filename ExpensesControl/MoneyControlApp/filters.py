import django_filters as dfilters
from datetime import date, timedelta

from .models import Operation

def get_choices():
    DATE_CHOICES = (
    ('День', 'Сегодня'),
    ('Неделя', 'Неделя'),
    ('Месяц', 'Месяц'),
    ('Год', 'Год'),
    )
    return DATE_CHOICES


class OperationsFilter(dfilters.FilterSet):
    date = dfilters.ChoiceFilter(choices=get_choices, method="date_filter", empty_label="Все время")

    @staticmethod
    def date_filter(queryset, name, value):
        if value == "День":
            return queryset.filter(date=date.today())
        elif value == "Неделя":
            week_start = date.today() - timedelta(days=date.today().weekday())
            week_end = week_start + timedelta(days=6)
            return queryset.filter(date__gte=week_start, date__lte=week_end)
        elif value == "Месяц":
            return queryset.filter(date__year=date.today().year, date__month=date.today().month)
        elif value == "Год":
            return queryset.filter(date__year=date.today().year)

        return queryset.all()
    
    class Meta:
        model = Operation
        fields = ('category',)

    