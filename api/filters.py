from django_filters import rest_framework as filters

from .models import Title


class TitleFilterBackend(filters.FilterSet):

    genre = filters.CharFilter(
        field_name='genre', lookup_expr='slug',
    )
    category = filters.CharFilter(
        field_name='category', lookup_expr='slug',
    )
    name = filters.CharFilter(
        field_name='name', lookup_expr='icontains'
    )

    class Meta:
        model = Title
        fields = ('genre', 'category', 'year', 'name')
