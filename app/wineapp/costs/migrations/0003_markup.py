# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('costs', '0002_costs_valuetype'),
    ]

    operations = [
        migrations.CreateModel(
            name='markup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=250)),
                ('value', models.CharField(max_length=25)),
                ('comments', models.CharField(max_length=250, blank=True)),
                ('date', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Markup',
                'verbose_name_plural': 'Markup',
            },
        ),
    ]
