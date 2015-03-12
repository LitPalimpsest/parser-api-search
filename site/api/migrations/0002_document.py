# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Document',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('docid', models.CharField(max_length=96)),
                ('title', models.TextField()),
                ('url', models.CharField(max_length=128, null=True)),
                ('pubdate', models.DateField(null=True)),
                ('type', models.CharField(max_length=32, null=True)),
                ('author', models.TextField(null=True)),
                ('majlang', models.CharField(max_length=3, null=True)),
                ('collection', models.ForeignKey(default=0, to='api.Collection')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
