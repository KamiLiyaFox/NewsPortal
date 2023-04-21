from django_filters import FilterSet, CharFilter, RangeFilter, DateFromToRangeFilter, DateFilter
from .models import *
from django.forms import MultiWidget, DateTimeInput
from .views import *

class NewsFilter(FilterSet):
    date_pub_gte = DateFilter(
        field_name='date_pub',
        lookup_expr='gt',
        label='Дата',
        widget=DateTimeInput(
            format='%d-%m-%Y',
            attrs={'type': 'date'}, )
    )
    # date_pub_lte = DateTimeFilter(
    #     field_name='date_pub',
    #     lookup_expr='lte',
    #     label='Дата по',
    #     widget=DateTimeInput(
    #         format='%d-%m-%Y; %H:%M',
    #         attrs={'type': 'Date'}, )
    # )
    #teFromToRangeFilter()

    class Meta:
        model = News
        fields = {
            'name': ['icontains'],
            'category__name': ['contains'],
        }
