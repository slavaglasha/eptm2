from django import forms
from django.forms import inlineformset_factory, BaseInlineFormSet

from django.contrib.auth.models import User, Group

from work_profiles.models import Profile
from .models import Departure
from main_requests.models import MainRequest


class MainDepartureForm(forms.ModelForm):
    works = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Выполненные работы', 'rows': 4}),
                            max_length=500, help_text="Максимальная длинна сообщения  500 "
                                                      "символов.", initial="", label="Выполненные работы")
    about = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Дополнительная информация', 'rows': 2}),
                            max_length=500,
                            help_text="Максимальная длинна сообщения  500 "
                                      "символов.", initial="", label="Дополнительная информация", required=False)

    class Meta:
        model = Departure
        fields = ['start_datetime', 'end_datetime', 'execute_users', 'works', 'about']
        labels = {'start_datetime': 'Начало работ', 'end_datetime': 'Окончание работ', 'execute_users': 'Исполнители',
                  'works': 'Работы', 'about': 'Дополнительная информация'}

    def __init__(self, *args, **kwargs):
        user = "No user first"
        group = -1
        if kwargs.keys().__contains__('dep_user'):
            user = kwargs.pop('dep_user')  # передали из CustomDepartureFormSet
            group = user.groups.all()[0].id
        else:
            user = "No user"
        print("MainDepartureForm __штше__ user - {0} group_id -{1} ".format(user, group))
        super(MainDepartureForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance != None:
            print("dep_user - {0} pk -{1} ".format(user, instance.pk))
        else:
            print("dep_user - {0} none object} ".format(user))
        user_enabled = []
        group1 = Group.objects.get(id=1)
        print(group1.name)
        users = group1.user_set.all()

        users = User.objects.filter(groups__id__in=[1, 2])
        prof= Profile.objects.filter(user__in=users )
        self.fields['execute_users'].queryset = prof


        # for i_user in User.objects.all():
        #      if not(i_user.groups.filter(pk__in= [1,2]) is None):
        #          print(i_user.pk)
        #          user_enabled.append(i_user.pk)
        # self.fields['execute_users'].queryset = Profile.objects.filter(pk__in =user_enabled)#






class CustomFormSet(BaseInlineFormSet):
    def __init__(self):
        super().__init__(self)
        print("Init")


DeparturesFormSet = inlineformset_factory(MainRequest, Departure,
                                          form=MainDepartureForm, extra=0, can_delete=True)


class CustomDepartureFormSet(DeparturesFormSet):
    def __init__(self, *args, **kwargs):
        #  create a user attribute and take it out from kwargs
        # so it doesn't messes up with the other formset kwargs
        self.user = kwargs.pop('dep_user')  # нужно передать во View при создании формы
        print("CustomDepartureFormSet init")
        super(DeparturesFormSet, self).__init__(*args, **kwargs)
        self.queryset = self.queryset.order_by('pk')

    def _construct_form(self, *args, **kwargs):
        kwargs['dep_user'] = self.user
        print("_construct_form user - {0}".format(self.user))
        return super(CustomDepartureFormSet, self)._construct_form(*args, **kwargs)


