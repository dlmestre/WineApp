# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datadb', '0004_auto_20160713_1153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='eurhkd',
            options={'verbose_name': 'Currency - EUR to HKD', 'verbose_name_plural': 'Currency - EUR to HKD'},
        ),
        migrations.AlterModelOptions(
            name='usdhkd',
            options={'verbose_name': 'Currency - USD to HKD', 'verbose_name_plural': 'Currency - USD to HKD'},
        ),
    ]
