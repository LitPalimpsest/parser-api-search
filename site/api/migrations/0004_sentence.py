# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_page'),
    ]

    operations = [
        migrations.CreateModel(
            name='Sentence',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identifier', models.CharField(max_length=10)),
                ('text', models.TextField()),
                ('xml', models.TextField()),
                ('i_score', models.FloatField(null=True)),
                ('palsnippet', models.BooleanField(default=False)),
                ('page', models.ForeignKey(default=0, to='api.Page')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
