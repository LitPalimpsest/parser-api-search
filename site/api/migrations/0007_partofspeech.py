# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_locationmention'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartOfSpeech',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('tag', models.CharField(max_length=4)),
                ('description', models.CharField(max_length=40, null=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
