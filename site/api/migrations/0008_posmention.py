# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_partofspeech'),
    ]

    operations = [
        migrations.CreateModel(
            name='POSMention',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=128)),
                ('pos', models.ForeignKey(default=0, to='api.PartOfSpeech')),
                ('sentence', models.ForeignKey(default=0, to='api.Sentence')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
