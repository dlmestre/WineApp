# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0002_negoces_recommended_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='negoces',
            options={'verbose_name': 'Negoce'},
        ),
    ]
