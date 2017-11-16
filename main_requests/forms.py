from django import forms
from django.forms import SplitDateTimeWidget
from django.utils import timezone

from work_profiles.models import Profile
from .models import MainRequest

my_default_errors = {
    'required': 'Обязательное поле ',
    'invalid': 'Введите правильный формат '
}

date_default_errors = {
    'required': 'Обязательное поле ',
    'invalid': 'Введите правильный формат даты (11.11.2017)'
}
time_default_errors = {
    'required': 'Обязательное поле ',
    'invalid': 'Введите правильный формат времени (11.11.2017)'
}
datetime_default_errors = {
    'required': 'Обязательное поле ',
    'invalid': 'Введите правильный формат дата - время (11.11.2017 00:00)'
}


class newMainRequestForm(forms.ModelForm):
    about = forms.CharField(widget=forms.Textarea(), max_length=500, help_text="Максимальная длинна сообщения  500 "
                                                                               "символов.", initial="About")

    # request_dateTime = forms.SplitDateTimeField(input_date_formats=['%d.%m.%Y'],
    #                                             input_time_formats=['%H:%M'],
    #                                             widget=SplitDateTimeWidget(date_format='%d.%m.%Y',
    #                                                                        time_format='%H:%M'),
    #                                             initial=timezone.now,
    #                                             error_messages=datetime_default_errors
    #
    #                                             )

    class Meta:
        model = MainRequest
        fields = ['request_user', 'request_outer_User', 'request_outer_status','request_outer_department',
                  'request_dateTime', 'place','place_outer','about']
        labels = {'request_user': 'Заявитель', 'request_outer_User': 'Внешний заявитель',
                   'request_outer_status': 'Должность', 'request_outer_department': ' Подразделение',
                   'request_dateTime': 'Дата подачи заявки', 'about': 'О чем заявлено',
                   'place': 'Место', 'place_outer':'Места нет в системе'}


class filterForm(forms.Form):
    input_dateTime_start = forms.DateTimeField(required=False, label='Интервал')
    input_dateTime_end = forms.DateTimeField(required=False, label='')
    input_user = forms.ModelChoiceField(queryset=Profile.objects.all(), required=False, label='Пользователь')

    request_user = forms.ModelChoiceField(queryset=Profile.objects.all(), required=False)
    request_outer_user = forms.CharField(max_length=50, required=False)
    request_dateTime_start = forms.DateTimeField(required=False, label='Интервал')
    request_dateTime_end = forms.DateTimeField(required=False, label='')

    receive_user = forms.ModelChoiceField(queryset=Profile.objects.all(), required=False, label='Пользователь')
    receive_dateTime_start = forms.DateTimeField(required=False, label='Интервал')
    receive_dateTime_end = forms.DateTimeField(required=False, label='')

    close_user = forms.ModelChoiceField(queryset=Profile.objects.all(), required=False, label='Пользователь')
    close_dateTime_start = forms.DateTimeField(required=False, label='Интервал')
    close_dateTime_end = forms.DateTimeField(required=False, label='')
