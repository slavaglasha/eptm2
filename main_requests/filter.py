import django_filters
import django_filters.widgets
from django.forms import CheckboxSelectMultiple, NullBooleanSelect,CheckboxInput
from django.db import models

from .models import MainRequest
from work_profiles.models import Profile





class MainRequestFilter(django_filters.FilterSet):
    number = django_filters.NumberFilter(label='№',lookup_expr='exact')
    input_datetime = django_filters.DateTimeFromToRangeFilter(label='Дата вводда', lookup_expr='range', widget=django_filters.widgets.RangeWidget(attrs={'display': 'inline', 'class':'datetimepicker'}))
    input_user = django_filters.ModelChoiceFilter(label = 'Пользователь', lookup_expr='exact', queryset=Profile.objects.filter())

    request_dateTime = django_filters.DateTimeFromToRangeFilter(label='Дата подачи заявки', lookup_expr='range')
    request_user = django_filters.ModelChoiceFilter(label='Пользователь', lookup_expr='exact',
                                                  queryset=Profile.objects.filter())
    request_outer_User = django_filters.CharFilter(label='')

    receive_dateTime = django_filters.DateTimeFromToRangeFilter(label='Дата принятия',lookup_expr='rangdbe')
    receive_user = django_filters.ModelChoiceFilter(label = 'Пользователь', lookup_expr='exact', queryset=Profile.objects.filter())

    close_dateTime = django_filters.DateTimeFromToRangeFilter(label='Дата закрытия',lookup_expr='range')
    close_user =django_filters.ModelChoiceFilter(label = 'Пользователь', lookup_expr='exact', queryset=Profile.objects.filter())


    class Meta:
        model = MainRequest
        fields=['number','input_datetime','input_user','request_dateTime','request_user']

        filter_overrides = {

            models.BooleanField: {
                'filter_class': django_filters.BooleanFilter,
                'extra': lambda f: {
                    'widget': CheckboxInput,
                },
            },
        }



