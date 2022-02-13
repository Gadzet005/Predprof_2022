import django_filters as dfilters

from .models import Operation
from MainApp.models import Category

class OperationsFilter(dfilters.FilterSet):
    type = dfilters.ChoiceFilter(label="Тип", empty_label="Любой", choices=[("Расход", "Расход"), ("Доход", "Доход")],
                                 field_name='category__type')
    category = dfilters.ModelChoiceFilter(empty_label="Любая", queryset=Category.objects)
    date = dfilters.DateRangeFilter(label="Период", empty_label="Все время")
    date_begin = dfilters.DateFilter(label="Начало периода", field_name='date', lookup_expr='gte')
    date_end = dfilters.DateFilter(label="Конец периода", field_name='date', lookup_expr='lte')

    class Meta:
        model = Operation
        fields = ('type', 'category', 'date', 'date_begin', 'date_end')


class BaseOperationFilter(dfilters.FilterSet):
    type = dfilters.ChoiceFilter(label="Тип", empty_label="Любой", choices=[("Расход", "Расход"), ("Доход", "Доход")],
                                 field_name='category__type')
    date = dfilters.DateRangeFilter(label="Период", empty_label="Все время")
    date_begin = dfilters.DateFilter(label="Начало периода", field_name='date', lookup_expr='gte')
    date_end = dfilters.DateFilter(label="Конец периода", field_name='date', lookup_expr='lte')

    class Meta:
        model = Operation
        fields = ('type', 'date', 'date_begin', 'date_end')

class OperationFilter(BaseOperationFilter):
    category = dfilters.ModelChoiceFilter(empty_label="Любая", queryset=Category.objects)

    class Meta:
        model = Operation
        fields = ('type', 'category', 'date', 'date_begin', 'date_end')
