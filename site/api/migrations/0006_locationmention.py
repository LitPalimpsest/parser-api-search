# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_location'),
    ]

    operations = [
        migrations.CreateModel(
            name='LocationMention',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=128)),
                ('start_word', models.CharField(max_length=10)),
                ('end_word', models.CharField(max_length=10)),
                ('document', models.ForeignKey(default=0, to='api.Document')),
                ('location', models.ForeignKey(default=0, to='api.Location')),
                ('page', models.ForeignKey(default=0, to='api.Page')),
                ('sentence', models.ForeignKey(default=0, to='api.Sentence')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
