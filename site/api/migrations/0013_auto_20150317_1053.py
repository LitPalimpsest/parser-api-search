# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0012_auto_20150313_1631'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='location',
            name='geom',
        ),
        migrations.RemoveField(
            model_name='location',
            name='poly',
        ),
        migrations.RemoveField(
            model_name='location',
            name='ptype',
        ),
        migrations.AddField(
            model_name='location',
            name='point',
            field=django.contrib.gis.db.models.fields.PointField(srid=4326, null=True, db_column=b'geom'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='polygon',
            field=django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True, db_column=b'poly'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='location',
            name='polygon_type',
            field=models.CharField(max_length=32, null=True, db_column=b'ptype'),
            preserve_default=True,
        ),
    ]
