# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('costs', '0003_markup'),
    ]

    operations = [
        migrations.AlterField(
            model_name='costs',
            name='date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
