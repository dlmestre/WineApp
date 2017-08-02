# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='eurhkd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=25)),
                ('date', models.CharField(max_length=25)),
                ('works', models.CharField(max_length=25)),
            ],
        ),
        migrations.CreateModel(
            name='usdhkd',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('value', models.CharField(max_length=25)),
                ('date', models.CharField(max_length=25)),
                ('works', models.CharField(max_length=25)),
            ],
        ),
    ]
