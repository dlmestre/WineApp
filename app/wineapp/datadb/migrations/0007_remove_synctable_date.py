# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('datadb', '0006_synctable'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='synctable',
            name='date',
        ),
    ]
