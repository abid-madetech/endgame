from django_filters import rest_framework as filters
from .models import KSB

class KSBFilter(filters.FilterSet):
    type = filters.CharFilter(field_name='ksb_type__name', lookup_expr='iexact')
    completed = filters.BooleanFilter(field_name='completed')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = KSB
        fields = ['type', 'completed', 'name']