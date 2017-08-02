# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0003_auto_20160713_1153'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='negoces',
            options={'verbose_name': 'Negoce', 'verbose_name_plural': 'Negoce'},
        ),
    ]
