from django.db import models

# Create your models here.
class department(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=500)

    def __str__(self):
        return self.name