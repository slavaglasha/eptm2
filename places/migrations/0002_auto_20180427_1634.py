# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-04-27 13:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='places',
            name='name',
            field=models.CharField(blank=True, help_text='Если у объекта есть названеи (станция)', max_length=200, null=True, verbose_name='Название станции'),
        ),
    ]