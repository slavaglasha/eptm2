from django import forms
from .models import  Places

class PlacesForm(forms.ModelForm):
    class Meta:
        model = Places
        fields  =['name','adres','geo_point','note','to_Place']

        labels = {'name': 'Название','adres':'Адрес', 'geo_point':'Отметка','note' :'Описание','to_Places':'Относится к месту'}
        help_texts={'adres':'Максимальная длинна 500 символовМаксимальная длинна 200 символов','geo_point':'Максимальная длинна 5 цифр','note':'Максимальная длинна 500 символов'}
        widgets = {'name':forms.TextInput,'adres':forms.Textarea(attrs={'placeholder': 'Адрес', 'rows':2}), 'note':forms.Textarea(attrs={'placeholder': 'Адрес', 'rows':2})}
