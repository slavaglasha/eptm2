from django.db import models

# Create your models here.
class Places(models.Model):
    name = models.CharField(max_length=200, null=True, blank=True, verbose_name='Название станции', help_text='Если у объекта есть названеи (станция)'    )
    adres =  models.CharField(max_length=200, null=True, unique=False, blank=True)
    geo_point = models.DecimalField(max_digits=5, decimal_places=2,null=True, blank=True)
    note = models.CharField(max_length=500, null=True, blank=True)
    to_Place = models.ForeignKey('self',related_name='places', verbose_name='Относится к станции', null=True, blank=True)

    def __str__(self):
        if self.adres is not None:
            return "%s %s " %(self.name,self.adres)
        else:
            return "%s " % (self.name)

    class Meta:
        verbose_name = "Место"
        verbose_name_plural = "Обьекты"

    @property
    def to_dict(selfe):

        return{'id':selfe.id,
               'name':selfe.name,
               'adres':selfe.adres,
               'geo_point':selfe.geo_point,
               'note':selfe.note,
               'to_place':'' if selfe.to_Place==None else selfe.to_Place.name
               }

    def clean(self):
        print('Geo point model', self.geo_point)
