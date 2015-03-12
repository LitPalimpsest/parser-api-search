# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.contrib.gis.db.models.fields


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_sentence'),
    ]

    operations = [
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=128)),
                ('lat', models.FloatField(null=True)),
                ('lon', models.FloatField(null=True)),
                ('geom', django.contrib.gis.db.models.fields.PointField(srid=4326, null=True)),
                ('poly', django.contrib.gis.db.models.fields.PolygonField(srid=4326, null=True)),
                ('ptype', models.CharField(max_length=32, null=True)),
                ('in_country', models.CharField(max_length=2, null=True)),
                ('gazref', models.CharField(max_length=32, null=True)),
                ('feature_type', models.CharField(max_length=32, null=True)),
                ('pop_size', models.BigIntegerField(null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
