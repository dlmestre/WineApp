# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datadb', '0003_auto_20160713_1149'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='usdhkd',
            options={'verbose_name': 'Currency - USD to HKD'},
        ),
    ]
