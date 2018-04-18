from django import forms
from django.forms import SplitDateTimeWidget, inlineformset_factory
from django.utils import timezone


from work_profiles.models import Profile
from places.models import  Places
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
    about = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'О чем заявлено', 'rows':4}), max_length=500, help_text="Максимальная длинна сообщения  500 "
                                                                               "символов.", initial="",label="О чем заявлено" )

    # request_dateTime = forms.SplitDateTimeField(input_date_formats=['%d.%m.%Y'],
    #                                             input_time_formats=['%H:%M'],
    #                                             widget=SplitDateTimeWidget(date_format='%d.%m.%Y',
    #                                                                        time_format='%H:%M'),
    #                                             initial=timezone.now,
    #                                             error_messages=datetime_default_errors
    #
    #                                             )
    request_dateTime = forms.DateTimeInput(attrs={'data-timepicker':'true', 'data-time-format':'hh:ii'})

    class Meta:

        model = MainRequest
        fields = ['request_user', 'request_outer_User', 'request_outer_status','request_outer_department',
                  'request_dateTime', 'place','about']
        labels = {'request_user': 'Заявитель', 'request_outer_User': 'Внешний заявитель',
                   'request_outer_status': 'Должность', 'request_outer_department': ' Подразделение',
                   'request_dateTime': 'Дата подачи заявки',
                   'place': 'Место', 'about': 'О чем заявлено', }
        error_messages = {'request_dateTime' : datetime_default_errors}

 #Запрет редактировать пользователя исполнителям
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user')
        super(newMainRequestForm, self).__init__(*args, **kwargs)
        groups = user.groups.all().values_list('id', flat=True)
        print(groups)
        print(3 in groups)

        if 3 in groups:
            self.fields['request_outer_status'].widget.attrs['readonly'] = True
            self.fields['request_outer_department'].widget.attrs['readonly'] = True
            self.fields['request_user'].widget.attrs['readonly'] = True
            self.fields['request_outer_User'].widget.attrs['readonly'] = True









class updateMainRequestForm(forms.ModelForm):
    about = forms.CharField(widget=forms.Textarea(attrs={'rows':4}), max_length=500, help_text="Максимальная длинна сообщения  500 "
                                                                               "символов.")



    class Meta:
        model = MainRequest

        fields = ['input_user','request_user', 'request_outer_User', 'request_outer_status', 'request_outer_department',
              'request_dateTime', 'place', 'about','receive_user','receive_dateTime', 'close_user', 'close_dateTime']
        labels = {'input_user':'Ввел заявку','request_user': 'Заявитель', 'request_outer_User': 'Внешний заявитель',
              'request_outer_status': 'Должность', 'request_outer_department': ' Подразделение',
              'request_dateTime': 'Дата подачи заявки', 'about': 'О чем заявлено',
              'place': 'Место',
              'receive_user':'Принял','receive_dateTime':'Дата принятия',
             'close_user':'Закрыл', 'close_dateTime':'Дата закрытия'}



    def __init__(self, *args, **kwargs):
        user = kwargs.pop('place_user')
        super(updateMainRequestForm, self).__init__( *args, **kwargs)
        instance = getattr(self, 'instance', None)
        print(instance.input_user.pk)
        groups = user.groups.all().values_list('id', flat=True)
        self.fields['receive_user'].queryset = Profile.objects.filter(user__groups__in=[1,2])
        self.fields['close_user'].queryset = Profile.objects.filter(user__groups__in=[1, 2])
        self.fields['input_user'].widget.attrs['readonly'] = True

        if 2 in groups:  # исполнители

            if instance.input_user.pk != user.id: #корректирует не сво. заявку мо;ет только принять
                self.fields['request_user'].widget.attrs['readonly'] = True
                self.fields['request_outer_User'].widget.attrs['readonly'] = True
                self.fields['request_outer_status'].widget.attrs['readonly'] = True
                self.fields['request_outer_department'].widget.attrs['readonly'] = True
                self.fields['request_dateTime'].widget.attrs['readonly'] = True
                self.fields['place'].widget.attrs['readonly'] = True
                self.fields['about'].widget.attrs['readonly'] = True
                self.fields['place'].widget.attrs['readonly'] = True
            if  instance.receive_user is not None:
                if instance.receive_user.id != user.id:
                    self.fields['receive_user'].widget.attrs['readonly'] = True
                    self.fields['receive_dateTime'].widget.attrs['readonly'] = True
                else:
                    self.fields['receive_user'].queryset = Profile.objects.filter(pk=user.id)  # можно поставить только себя
            else:
                self.fields['receive_user'].queryset = Profile.objects.filter(pk=user.id)  # можно поставить только себя

            self.fields['close_user'].widget.attrs['readonly'] = True
            self.fields['close_dateTime'].widget.attrs['readonly'] = True

            if instance.is_closed:
                self.fields['request_user'].widget.attrs['readonly'] = True
                self.fields['request_outer_User'].widget.attrs['readonly'] = True
                self.fields['request_outer_status'].widget.attrs['readonly'] = True
                self.fields['request_outer_department'].widget.attrs['readonly'] = True
                self.fields['request_dateTime'].widget.attrs['readonly'] = True
                self.fields['place'].widget.attrs['readonly'] = True
                self.fields['about'].widget.attrs['readonly'] = True
                self.fields['place'].widget.attrs['readonly'] = True
                self.fields['receive_user'].widget.attrs['readonly'] = True
                self.fields['receive_dateTime'].widget.attrs['readonly'] = True



        if 3 in groups: #пользователи
            self.fields['receive_user'].widget.attrs['readonly'] = True
            self.fields['receive_dateTime'].widget.attrs['readonly'] = True

            self.fields['close_user'].widget.attrs['readonly'] = True
            self.fields['close_dateTime'].widget.attrs['readonly'] = True
            self.fields['request_user'].widget.attrs['readonly'] = True
            self.fields['request_outer_User'].widget.attrs['readonly'] = True
            self.fields['request_outer_status'].widget.attrs['readonly'] = True
            self.fields['request_outer_department'].widget.attrs['readonly'] = True
            print("user pk - input_pk -  ",instance.input_user.user.id,user.id, )

            if instance.input_user.user.id != user.id or instance.receive_user is not None or instance.is_closed:


                self.fields['request_dateTime'].widget.attrs['readonly'] = True
                self.fields['place'].widget.attrs['readonly'] = True
                self.fields['about'].widget.attrs['readonly'] = True
                self.fields['place'].widget.attrs['readonly'] = True


        # self.fields['sku'].widget.attrs['readonly'] = True




class filterForm(forms.Form):

    input_dateTime_start = forms.DateTimeField(required=False, label='Интервал' )
    input_dateTime_end = forms.DateTimeField(required=False, label='')
    input_user = forms.ModelChoiceField(queryset=Profile.objects.all(), required=False, label='Пользователь')

    request_user = forms.ModelChoiceField(queryset=Profile.objects.all(), required=False)
    request_outer_user = forms.CharField(max_length=50, required=False)
    request_dateTime_start = forms.DateTimeField(required=False, label='Интервал')
    request_dateTime_end = forms.DateTimeField(required=False, label='')
    place = forms.ModelChoiceField(queryset=Places.objects.all().order_by('name'),required=False, label='Место')

    receive_user = forms.ModelChoiceField(queryset=Profile.objects.all(), required=False, label='Пользователь')
    receive_dateTime_start = forms.DateTimeField(required=False, label='Интервал')
    receive_dateTime_end = forms.DateTimeField(required=False, label='')

    close_user = forms.ModelChoiceField(queryset=Profile.objects.all(), required=False, label='Пользователь')
    close_dateTime_start = forms.DateTimeField(required=False, label='Интервал')
    close_dateTime_end = forms.DateTimeField(required=False, label='')
