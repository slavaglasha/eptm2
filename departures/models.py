from django.db import models

from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from places.models import Places
from main_requests import models as main_request_model
from work_profiles.models import Profile
from django.utils.timezone import localtime

# Create your models here.


class Departure(models.Model):
    main_request = models.ForeignKey(main_request_model.MainRequest, related_name='+',verbose_name='Заявка', null=False)
    input_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False, verbose_name='Дата ввода')
    start_datetime = models.DateTimeField(null=True, blank=True, default=timezone.now, verbose_name='Начало работ')
    end_datetime = models.DateTimeField(auto_now_add=False, null=True, blank=True, verbose_name='Окончание работ')
    input_user = models.ForeignKey(Profile, related_name='Departure_input_user', null=False, blank=False, verbose_name='Ввел')
    works = models.CharField(max_length=1000, null=False, help_text='Выполненные работы' ) #error_messages='Нужно ввести что сделано'
    about = models.CharField(max_length=1000,null=True, blank=True,  help_text="Максимальная дллина 1000 символов",verbose_name='Дополнительная информация')
    execute_users = models.ManyToManyField(Profile,related_name='departure_execute_users',  blank=False, help_text='Принимали участие в работе',verbose_name='Исполнители')

    __old_start_datetime= None
    __old_end_date = None

    class Meta:
        verbose_name = "Выезд оснновной заявки"
        verbose_name_plural = "Выезды"

    def __str__(self):
        return '{0} - Заявка # {1}'.format(self.input_datetime, self.main_request.number)

    def __init__(self, *args, **kwargs):
        super(Departure, self).__init__(*args, **kwargs)
        print("init")
        print(self.input_datetime)

        self.__old_start_datetime = self.input_datetime
        self.__old_end_date = self.end_datetime

    def clean(self):
        print("Clean Departure {0}".format(self.pk))
        tomorrow = timezone.now().__add__(timedelta(days=2))
        yesterday = timezone.now().__add__(timedelta(days=-1))

        print("time now-{0}".format(localtime(timezone.now())))
        errors = {}
        print('valid', self.get_deferred_fields().__len__())
        print("clean")

        #

        if (self.pk is None) :
            print( "new departure")
            origin = None
        else:
            origin = Departure.objects.get(pk=self.pk)
        if (self.start_datetime is None):
              errors['start_datetime'] = 'Нужно ввести дату начала работ'
        else:
            if origin is not  None:
                print('origin_start-',localtime(origin.start_datetime).strftime('%d.%m.%Y %H:%M'))
                if (origin.start_datetime!=self.start_datetime):
                    print('start date is changed')
                    if (self.start_datetime<yesterday):
                        errors['start_datetime'] = 'Дата начала работ не может быть меньше ' + localtime(
                            yesterday).strftime('%d.%m.%Y %H:%M')

            print()
            if (origin is None):
                  if (self.start_datetime<yesterday):
                      errors['start_datetime'] = 'Дата начала работ не может быть меньше '+localtime(yesterday).strftime('%d.%m.%Y %H:%M')
            if (self.start_datetime>tomorrow):
                      errors['start_datetime'] = 'Дата начала работ не может быть больше ' +localtime(tomorrow).strftime('%d.%m.%Y %H:%M')
        #
        #
        # if ('end_datetime' in self.get_deferred_fields()):
        #      if ((self.start_datetime) < yestarday):
        #          errors['end_datetime'] = 'Дата окончания работ не может быть меньше ' + yestarday
        if not(self.end_datetime is None):
            if ((self.end_datetime) > tomorrow):
                  errors['end_datetime'] = 'Дата окончания работ не может быть больше ' + localtime(tomorrow).strftime('%d.%m.%Y %H:%M')



        #disp_users = ''
        # for user in   self.execute_users.all():
        #     if user.user.groups.id == 3:
        #         disp_users += user+'; '
        # if disp_users!='':
        #     errors['execute_users'] = 'Gjkmpjdfntkb '+disp_users + ' не могут быть исполнителями'
        if len(errors)>0:
            raise ValidationError(errors)

