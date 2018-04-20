from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from departments.models import department
from django.dispatch import receiver


# Create your models here.
# related_name используется для доступа в другую сторону user - model User p = user.profileEptm
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profileEptm')
    deparment = models.ForeignKey(department)
    user_position = models.CharField(max_length=200, null=False, blank=True)


    def __str__(self):
        return self.user.last_name+' '+self.user.first_name

    @property
    def user_group_first_id(self):
        return self.user.groups.all()[0].id

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):

        instance.profileEptm.save()
