from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime

from places.models import Places
from work3.settings import DATETIME_INPUT_FORMATS
from work_profiles.models import Profile


class MainRequest(models.Model):
    number = models.IntegerField(null=True, blank=True)
    input_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    input_user = models.ForeignKey(Profile, related_name='mainRequestInput', null=False, blank=True,
                                    on_delete=models.PROTECT)
    request_dateTime = models.DateTimeField(null=True, blank=True, default=timezone.now)
    request_user = models.ForeignKey(Profile, related_name='mainRequestRequest', null=True, blank=True,
                                     help_text="Можно сохранить данные не из списка",
                                     on_delete=models.PROTECT)
    request_outer_User = models.CharField(max_length=100, null=True, blank=True,
                                          help_text='От кого фактически пришла не из системы ФИО')
    request_outer_status = models.CharField(max_length=100, null=True, blank=True)
    request_outer_department = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(max_length=1000, null=False)
    receive_dateTime = models.DateTimeField(null=True, blank=True)
    receive_user = models.ForeignKey(Profile, related_name='mainRequestReceive', null=True, blank=True,
                                     on_delete=models.PROTECT)
    close_dateTime = models.DateTimeField(null=True, blank=True)
    close_user = models.ForeignKey(Profile, related_name='mainRequestClose', null=True, blank=True,
                                   on_delete=models.PROTECT)
    place = models.ForeignKey(Places, related_name='main_requests_places', null=True, blank=True,
                                on_delete=models.PROTECT)
    place_outer = models.CharField(max_length=200, null=True, blank=True)
    changed_datetime = models.DateTimeField(auto_now=True, null=False, blank=False)

    class Meta:
        verbose_name = "Главная заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return '{0} - {1}'.format(self.input_datetime.year, self.number)

    def clean(self):
        tomorrow = timezone.now().__add__(timedelta(days=1))
        yesterday = timezone.now().__add__(timedelta(days=-1))
        errors = {}
        origin = None
        if self.pk is not None:
            origin = MainRequest.objects.get(pk=self.pk)
        if (self.request_user is None) and (self.request_outer_User is None):
            errors['request_user'] = 'Нужно ввести заявителя.'
            errors['request_outer_User'] = 'Нужно ввести заявителя!'

        if (self.request_user is None) and (self.request_outer_department is None):
            errors['request_outer_department'] = 'Нужно ввести подразделение заявителя!'
        if (self.request_user is None) and (self.request_outer_status is None):
            errors['request_outer_status'] = 'Нужно ввести должность заявителя!'
        if (self.place_outer is None) and (self.place is None):
            errors['place'] = 'Нужно ввести место!'
        if self.pk is None:
            if self.request_dateTime < yesterday:
                errors['request_dateTime'] = 'Не может быть раньше ' + localtime(yesterday).strftime('%d.%m.%Y %H:%M')
        if self.request_dateTime > tomorrow:
            errors['request_dateTime'] = 'Не может быть позже ' + localtime(tomorrow).strftime('%d.%m.%Y %H:%M')
        if origin is not None:
            if timezone.localtime(self.request_dateTime).strftime(
                    DATETIME_INPUT_FORMATS[0]) != timezone.localtime(origin.request_dateTime).strftime(
                        DATETIME_INPUT_FORMATS[0]):
                if self.request_dateTime < yesterday:
                    errors['request_dateTime'] = 'Не может быть раньше ' + localtime(yesterday).strftime(
                        '%d.%m.%Y %H:%M')
        if (self.receive_dateTime is None) and (self.receive_user is not None):
            errors['receive_dateTime'] = ' Нужно ввести  дату принятия  заявки!'
        if (self.receive_user is None) and (self.receive_dateTime is not None):
            errors['receive_user'] = ' Нужно ввести   пользоваеля принявшего заявку!'
        if (self.close_dateTime is None) and (self.close_user is not None):
            errors['close_dateTime'] = 'Дата закрытия  заявки должна быть определена!'
        if (self.close_dateTime is not None) and (self.close_user is None):
            errors['close_user'] = 'Пользоваель закрывший  заявку должен быть определен!'

        if (self.receive_dateTime is not None) and (self.receive_user is None):
            errors['close_user'] = "Пользоваель принявший  заявку должен быть определен!"
        if self.receive_dateTime is not None:
            if self.receive_dateTime > tomorrow:
                errors['receive_dateTime'] = 'Не может быть позже ' + localtime(tomorrow).strftime('%d.%m.%Y %H:%M')
            if origin is None:
                if self.receive_dateTime < yesterday:
                    errors['receive_dateTime'] = 'Не может быть раньше ' + localtime(yesterday).strftime(
                        '%d.%m.%Y %H:%M')
                    # else:
                    #     if timezone.localtime(origin.receive_dateTime) != timezone.localtime(self.receive_dateTime):
                    #         if self.receive_dateTime < yesterday:
                    #             errors['receive_dateTime'] = 'Не может быть раньше ' + localtime(yesterday).strftime(
                    #                 '%d.%m.%Y %H:%M')
        if (self.close_dateTime is not None) and (self.receive_user is None or self.request_dateTime is None):
            errors['close_dateTime'] = "Нужно сначала принять заявку!"
        if (self.close_user is not None) and (self.receive_user is None or self.request_dateTime is None):
            errors['close_user'] = "Нужно сначала принять заявку!"
        if self.receive_dateTime is not None and self.close_dateTime is not None:
            if self.receive_dateTime > self.close_dateTime:
                errors['close_dateTime'] = "Дата закрытия заявки должна быть больше даты ее принятия!"

        # if self.close_dateTime is not None:
        #     if self.close_dateTime > tomorrow:
        #         errors['close_dateTime'] = 'Не может быть позже ' + localtime(tomorrow).strftime(
        #             DATETIME_INPUT_FORMATS[0])

        if self.close_dateTime is not None or self.close_user is not None:
            if self.departure_set.filter(end_datetime__isnull=True).__len__() > 0:
                if 'close_dateTime' in errors:
                    errors['close_dateTime'].join(' Нужно закрыть все выезды а затем закрыть заявку!')
                else:
                    errors['close_dateTime'] = 'Нужно закрыть все выезды а затем закрыть заявку!'

        # print(errors)
        if len(errors) > 0:
            raise ValidationError(errors)

    @property
    def str_receive_dateTime(self):
        if self.receive_dateTime is None:
            return ''
        else:
            return timezone.localtime(self.receive_dateTime).strftime(DATETIME_INPUT_FORMATS[0])

    @property
    def str_close_dateTime(self):
        if self.close_dateTime is None:
            return ''
        else:
            return timezone.localtime(self.close_dateTime).strftime(DATETIME_INPUT_FORMATS[0])

    @property
    def str_user_request(self):
        if self.request_user is not None:
            return self.request_user.user.first_name + ' ' + self.request_user.user.last_name
        else:
            return self.request_outer_User

    @property
    def str_user_deparment(self):
        if self.request_user is not None:
            if self.request_user.deparment is None:
                return ''
            else:
                return self.request_user.deparment.name
        else:
            return self.request_outer_department

    @property
    def str_user_status(self):
        if self.request_user is not None:
            if self.request_user.user_position is None:
                return ''
            else:
                return self.request_user.user_position
        else:
            return self.request_outer_status

    @property
    def is_closed(self):
        if self.close_user is not None and self.close_dateTime is not None:
            return True
        else:
            return False
    @property
    def is_recived(self):
        return self.receive_dateTime is not None and self.receive_user is not None

    @property
    def status(self):
        if self.is_recived:
            return 1
        if self.is_closed :
           # print('isclosed')
            return 2
        return 0

    # для преобразования в json
    @property
    def to_dict(self):
        if self.place is None:
            pl = ''
        else:
            pl = self.place.name
        return {"id": self.id,
                "number": self.number,
                "about": self.about,
                "request_dateTime": timezone.localtime(self.request_dateTime).strftime(DATETIME_INPUT_FORMATS[0]),
                "str_user_request": self.str_user_request,
                "str_user_status": self.str_user_status,
                "str_user_deparment": self.str_user_deparment,
                "place": pl,
                "receive-user-name": '' if self.receive_user is None else self.receive_user.user.first_name,
                "str_receive_dateTime": self.str_receive_dateTime,
                "close-user-name": '' if self.close_user == None else self.close_user.user.first_name,
                "str_close_dateTime": self.str_close_dateTime
                }

    def can_save(self, request_user):
        group_user = request_user.groups.all().values_list('id', flat=True)

        if 1 in group_user:
            return True
        if 2 in group_user:
            if self.is_closed:

                return False
            else:

                return True
        if 3 in group_user:
            if self.is_closed:
                return False
            else:
                if self.input_user.user.pk == request_user.pk and self.receive_user is None:
                    return True
                else:
                    return False

    def can_add_dep(self, request_user):
        group_user = request_user.groups.all().values_list('id', flat=True)
        if self.close_dateTime is not None or self.close_dateTime is not None:
            return False

        if 3 in group_user:
            return False

        if 2 in group_user:
            return True
        if 1 in group_user:
            return True
