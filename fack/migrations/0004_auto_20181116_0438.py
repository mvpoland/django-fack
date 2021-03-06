# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2018-11-16 04:38
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fack', '0003_auto_20170403_0543'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionscore',
            name='ip_address',
            field=models.GenericIPAddressField(blank=True, null=True, verbose_name='IP address'),
        ),
        migrations.AlterField(
            model_name='questionscore',
            name='score',
            field=models.IntegerField(choices=[(0, 'No'), (1, 'Yes')], default=1, verbose_name='score'),
        ),
        migrations.AlterField(
            model_name='topic',
            name='icon',
            field=models.ImageField(blank=True, null=True, upload_to='topic_icons/'),
        ),
    ]
