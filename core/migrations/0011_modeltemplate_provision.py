# -*- coding: utf-8 -*-
# Generated by Django 1.11.4 on 2017-09-27 04:01
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20170922_0206'),
    ]

    operations = [
        migrations.AddField(
            model_name='modeltemplate',
            name='provision',
            field=models.TextField(blank=True, null=True),
        ),
    ]
