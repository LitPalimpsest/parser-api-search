# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0011_auto_20150313_1320'),
    ]

    operations = [
        migrations.AlterField(
            model_name='locationmention',
            name='location',
            field=models.ForeignKey(related_name='location-mentions', default=0, to='api.Location'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='document',
            field=models.ForeignKey(related_name='pages', to='api.Document'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='sentence',
            name='page',
            field=models.ForeignKey(related_name='sentences', default=0, to='api.Page'),
            preserve_default=True,
        ),
    ]
