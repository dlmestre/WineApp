# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='negoces',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('wine', models.CharField(max_length=50)),
                ('price', models.CharField(max_length=10)),
                ('date', models.CharField(max_length=50)),
                ('year', models.CharField(max_length=10)),
                ('region', models.CharField(max_length=50)),
                ('format', models.CharField(max_length=10)),
                ('markup_price', models.CharField(max_length=10)),
                ('markup_percentile', models.CharField(max_length=10)),
                ('ws_merchants', models.CharField(max_length=200)),
                ('ws_price', models.CharField(max_length=10)),
                ('negoce_name', models.CharField(max_length=200)),
            ],
        ),
    ]
