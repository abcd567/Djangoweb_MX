# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2019-03-17 22:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_auto_20190317_2147'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='birday',
            field=models.DateField(blank=True, null=True, verbose_name='\u751f\u65e5'),
        ),
    ]
