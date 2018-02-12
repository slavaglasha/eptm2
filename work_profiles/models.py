from django.db import models
from django.contrib.auth.models import User
from departments.models import department


# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profileEptm')
    deparment = models.ForeignKey(department)
    user_position = models.CharField(max_length=200, null=False, blank=True)


    def __str__(self):
        return self.user.last_name+' '+self.user.first_name

    @property
    def user_group_first_id(self):
        return self.user.groups.all()[0].id
