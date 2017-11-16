from datetime import timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone

from places.models import Places
from work_profiles.models import Profile


class MainRequest(models.Model):
    number = models.IntegerField(null=True, blank=True)
    input_datetime = models.DateTimeField(auto_now_add=True, null=False, blank=False)
    input_user = models.ForeignKey(Profile, related_name='mainRequestInput', null=False, blank=True)
    request_dateTime = models.DateTimeField(null=True, blank=True, default=timezone.now)
    request_user = models.ForeignKey(Profile, related_name='mainRequestRequest', null=True, blank=True)
    request_outer_User = models.CharField(max_length=100, null=True, blank=True,
                                          help_text='От кого фактически пришла не из системы ФИО')
    request_outer_status = models.CharField(max_length=100, null=True, blank=True)
    request_outer_department = models.CharField(max_length=100, null=True, blank=True)
    about = models.TextField(max_length=1000, null=False)
    receive_dateTime = models.DateTimeField(null=True, blank=True)
    receive_user = models.ForeignKey(Profile, related_name='mainRequestReceive', null=True, blank=True)
    close_dateTime = models.DateTimeField(null=True, blank=True)
    close_user = models.ForeignKey(Profile, related_name='mainRequestClose', null=True, blank=True)
    place = models.ForeignKey(Places, related_name='main_requests_places', null=True, blank=True)
    place_outer = models.CharField(max_length=200, null=True, blank=True)

    class Meta:
        verbose_name = "Главная заявка"
        verbose_name_plural = "Заявки"

    def __str__(self):
        return '{0} - {1}'.format(self.input_datetime.year, self.number)

    def clean(self):
        tomorrow = timezone.now().__add__(timedelta(days=2))
        yestarday = timezone.now().__add__(timedelta(days=-1))

        if (self.request_user is None) and (self.request_outer_User is None):
            raise ValidationError(
                {'request_user': 'Нужно ввести заявителя.', 'request_outer_User': 'Нужно ввести заявителя!'})
        if (self.request_user is None) and (self.request_outer_department is None):
            raise ValidationError({'request_outer_department': 'Нужно ввести подразделение заявителя!'})
        if (self.request_user is None) and (self.request_outer_status is None):
            raise ValidationError({'request_outer_department': 'Нужно ввести должность заявителя!'})
        if (self.place_outer is None) and (self.place is None):
            raise ValidationError({'place': 'Нужно ввести место!', 'place_outer': 'Нужно ввести место!'})
        if ('request_dateTime' in self.get_deferred_fields()) or (self.pk is None):
            if self.request_dateTime < yestarday:
                raise ValidationError({'request_dateTime': 'Не может быть раньше  вчера'})
        if self.request_dateTime > tomorrow:
            raise ValidationError({'request_dateTime': 'Не может быть позже завтра'})
        if ((self.receive_dateTime is None) and (self.receive_user is not None)) or (
                    (self.receive_dateTime is not None) and (self.receive_user is None)):
            raise ValidationError(
                {'receive_user': 'Дата принятия и пользоваель принявший заявку должны быит определены!'})
        if ((self.close_dateTime is None) and (self.close_user is not None)) or (
                    (self.receive_dateTime is not None) and (self.receive_user is None)):
            raise ValidationError(
                {'close_user': 'Дата закрытия и пользоваель закрывший  заявку должны быит определены!'})

    @property
    def str_receive_dateTime(self):
        if self.receive_dateTime is None:
            return ''
        else:
            return self.receive_dateTime

    @property
    def str_close_dateTime(self):
        if self.close_dateTime is None:
            return ''
        else:
            return self.close_dateTime

    @property
    def str_user_request(self):
        if self.request_user is not None:
            return self.request_user.user.first_name+' '+self.request_user.user.last_name
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
