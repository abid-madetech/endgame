from django_filters import rest_framework as filters
from .models import KSB

class KSBFilter(filters.FilterSet):
    ksb_type = filters.NumberFilter()  # Automatically maps to `ksb_type_id`
    completed = filters.BooleanFilter()
    name = filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = KSB
        fields = ['ksb_type', 'completed', 'name']