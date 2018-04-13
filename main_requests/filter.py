import django_filters
import django_filters.widgets
from django.forms import CheckboxSelectMultiple, NullBooleanSelect,CheckboxInput, NumberInput
from django.db import models

from .models import MainRequest
from work_profiles.models import Profile


class MyRangeWidget(django_filters.widgets.RangeWidget):

    def format_output(self, rendered_widgets):
        # Method was removed in Django 1.11.
        return '<span>-</span>'.join(rendered_widgets)

class HelpfulFilterSet(django_filters.FilterSet):
    @classmethod
    def filter_for_field(cls, f, name, lookup_expr):
        filter = super(HelpfulFilterSet, cls).filter_for_field(f, name, lookup_expr)
        filter.extra['help_text'] = f.help_text

        return filter





class MainRequestFilter(HelpfulFilterSet):
    number = django_filters.NumberFilter(label='№',lookup_expr='exact',widget = NumberInput(attrs={'new_line':'true'}))
    input_datetime = django_filters.DateTimeFromToRangeFilter(label='Дата вводда', lookup_expr='range', widget=MyRangeWidget(attrs={'display': 'inline', 'class':'datepicker-need'}))
    input_user = django_filters.ModelChoiceFilter(label = 'Пользователь', lookup_expr='exact', queryset=Profile.objects.filter() )

    request_dateTime = django_filters.DateTimeFromToRangeFilter(label='Дата подачи заявки', lookup_expr='range')
    request_user = django_filters.ModelChoiceFilter(label='Подал', lookup_expr='exact',
                                                  queryset=Profile.objects.filter(), help_text='Можно ввести с клавиатуры')
    request_outer_User = django_filters.CharFilter(label='')

    receive_dateTime = django_filters.DateTimeFromToRangeFilter(label='Дата принятия',lookup_expr='rangdbe')
    receive_user = django_filters.ModelChoiceFilter(label = 'Принял', lookup_expr='exact', queryset=Profile.objects.filter())

    close_dateTime = django_filters.DateTimeFromToRangeFilter(label='Дата закрытия',lookup_expr='range')
    close_user =django_filters.ModelChoiceFilter(label = 'Закрыл', lookup_expr='exact', queryset=Profile.objects.filter())



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



