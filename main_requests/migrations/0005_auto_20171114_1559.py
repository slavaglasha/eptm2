# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-14 13:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_requests', '0004_auto_20171114_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainrequest',
            name='request_outer_User',
            field=models.CharField(blank=True, help_text='От кого фактически пришла не из системы ФИО', max_length=100, null=True),
        ),
    ]
