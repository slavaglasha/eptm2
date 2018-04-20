from django.contrib.auth.models import User, Group
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from work_profiles.models import Profile

#для редактирования данніх
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
        labels = {'first_name':'Имя','last_name':'Фамилия','emain':'Email'}

#для добавления
class NewUserForm( forms.ModelForm ):
  username = forms.CharField(label='Логин',help_text='Максимальная длинна  30 символов.', max_length = 30 )
  firstname = forms.CharField( label ='Имя',max_length = 30, required = False )
  lastname = forms.CharField(label = 'Фамилия', max_length = 30, required = False )
  email = forms.CharField( max_length = 30 )
  pass1 = forms.CharField( widget = forms.PasswordInput, label = "Пароль", min_length = 6, max_length = 30, help_text='Длинна пароля от 6 до 30 символов ' )
  pass2 = forms.CharField( widget = forms.PasswordInput, label = "Пароль ещё раз" )
  group = forms.ModelChoiceField(queryset =Group.objects.all(), label = "Тип пользователя" )

  def clean_pass2(self):
    if (self.cleaned_data["pass2"] != self.cleaned_data.get("pass1", "")):
          raise forms.ValidationError("Пароли не совпадают")
    return self.cleaned_data["pass2"]


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('deparment', 'user_position')
        labels = {'deparment':'Департамент','user_position':'Долджность'}