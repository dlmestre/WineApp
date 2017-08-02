# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datadb', '0002_markup'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eurhkd',
            options={'verbose_name': 'Currency - EUR to HKD'},
        ),
    ]
