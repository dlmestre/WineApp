# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchants', '0016_negoces2_wineid'),
    ]

    operations = [
        migrations.AddField(
            model_name='negoces2',
            name='wine_chinese',
            field=models.CharField(default=b'', max_length=200, verbose_name=b'Wine (Chinese)'),
        ),
        migrations.AlterField(
            model_name='negoces2',
            name='wine',
            field=models.CharField(max_length=50, verbose_name=b'Wine (English)'),
        ),
    ]
