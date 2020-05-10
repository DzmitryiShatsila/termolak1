import django_filters
from .models import Cases


class CasesFilter(django_filters.FilterSet):
    class Meta:
        model = Cases
        fields = ('date', 'images', 'case', 'product', 'software', 'procedure')