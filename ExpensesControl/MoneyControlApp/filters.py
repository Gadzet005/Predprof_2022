import django_filters as dfilters

from .models import Operation

class OperationsFilter(dfilters.FilterSet):
    date = dfilters.DateRangeFilter(label="Период", empty_label="Все время")
    date_begin = dfilters.DateFilter(label="Начиная с", field_name='date', lookup_expr='gte')
    date_end = dfilters.DateFilter(label="до", field_name='date', lookup_expr='lte')

    class Meta:
        model = Operation
        fields = ('category', 'date')
