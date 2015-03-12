# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_document'),
    ]

    operations = [
        migrations.CreateModel(
            name='Page',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('url', models.URLField(null=True)),
                ('lang', models.CharField(max_length=16, null=True)),
                ('document', models.ForeignKey(to='api.Document')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
