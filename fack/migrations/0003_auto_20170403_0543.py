# -*- coding: utf-8 -*-
# Generated by Django 1.9.12 on 2017-04-03 03:43
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fack', '0002_auto_20151222_0952'),
    ]

    operations = [
        migrations.AlterField(
            model_name='topic',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created on'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='updated_on',
            field=models.DateTimeField(auto_now=True, verbose_name='updated on'),
        ),
    ]
