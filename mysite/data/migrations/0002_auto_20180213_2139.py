# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-02-13 23:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('data', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='file',
            field=models.FileField(upload_to='userdata/'),
        ),
    ]
