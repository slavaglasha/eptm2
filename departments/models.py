from django.db import models


# Create your models here.
class department(models.Model):
    name = models.CharField(max_length=30, unique=True)
    description = models.TextField(max_length=500)

    class Meta:
        verbose_name = 'Департамент'
        verbose_name_plural = 'Департаменты'

    def __str__(self):
        return self.name

    @property
    def to_dict(self):
        return {"id": self.id,
                "name": self.name,
                "description": self.description}
