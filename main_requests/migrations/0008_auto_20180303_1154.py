# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2018-03-03 09:54
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_requests', '0007_auto_20171114_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mainrequest',
            name='request_user',
            field=models.ForeignKey(blank=True, help_text='Можно сохранить данные не из списка', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='mainRequestRequest', to='work_profiles.Profile'),
        ),
    ]
