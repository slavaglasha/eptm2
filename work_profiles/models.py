from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.utils import timezone

from departments.models import department
from django.dispatch import receiver

# Create your models here.
# related_name используется для доступа в другую сторону user - model User p = user.profileEptm
from work3.settings import DATETIME_INPUT_FORMATS


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profileEptm')
    deparment = models.ForeignKey(department, null=True, blank=True)
    user_position = models.CharField(max_length=200, null=True, blank=True)


    def __str__(self):
        return self.user.last_name + ' ' + self.user.first_name

    def name(self):
        return self.user.username


    @property
    def  user_group_first(self):
        if self.user.groups.all().__len__() == 0:
            return  None
        else:
            return self.user.groups.all()[0]


    @property
    def user_group_first_id(self):
        if self.user.groups.all().__len__()==0:
            return -1
        return self.user.groups.all()[0].id

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
                Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.profileEptm.save()

    @property
    def to_dict(self):
        group_name = ''
        if self.user.groups.all().__len__() > 0:
            group_name = self.user.groups.all()[0].name

        return {'id': self.id,
                'username': self.user.username,
                'full_name': self.user.get_full_name(),
                'date_join': timezone.localtime(self.user.date_joined).strftime(DATETIME_INPUT_FORMATS[0]),
                'group_name': group_name,
                'user_department': '' if self.deparment is None else self.deparment.name,
                'user_position': self.user_position,
                }
