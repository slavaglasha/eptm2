from django import forms

from departments.models import department


class DepartmentForm(forms.ModelForm):
    class Meta:
        model = department
        fields = ['name', 'description']
        labels = {'name': 'Название', 'description': 'Описание'}
