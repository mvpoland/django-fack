# -*- coding: utf-8 -*-
from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fack', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questionscore',
            name='ip_address',
            field=models.GenericIPAddressField(null=True, verbose_name=b'IP address', blank=True),
            preserve_default=True,
        ),
    ]
