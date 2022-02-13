import django_filters as dfilters

from .models import Operation

class OperationsFilter(dfilters.FilterSet):
    date = dfilters.DateRangeFilter(label="Период", empty_label="Все время")
    date_begin = dfilters.DateFilter(label="От", field_name='date', lookup_expr='gte')
    date_end = dfilters.DateFilter(label="До", field_name='date', lookup_expr='lte')

    @classmethod
    def filter_for_field(cls, f, name, lookup_expr):
        print(f, name, lookup_expr)
        filter = super().filter_for_field(f, name, lookup_expr)
        filter.extra['help_text'] = f.help_text
        return filter

    class Meta:
        model = Operation
        fields = ('category', 'date')
