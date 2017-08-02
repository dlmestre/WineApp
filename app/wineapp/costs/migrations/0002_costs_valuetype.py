# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('costs', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='costs',
            name='valuetype',
            field=models.CharField(default='N', max_length=6),
            preserve_default=False,
        ),
    ]
