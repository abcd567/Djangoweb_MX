# -*- coding: utf-8 -*-
# Generated by Django 1.9.5 on 2019-02-27 22:59
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('organization', '0003_auto_20190226_2218'),
    ]

    operations = [
        migrations.RenameField(
            model_name='courseorg',
            old_name='course_nums',
            new_name='courses',
        ),
    ]