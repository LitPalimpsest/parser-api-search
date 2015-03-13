# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0010_auto_20150313_1129'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='collection',
            field=models.ForeignKey(related_name='documents', default=0, to='api.Collection'),
            preserve_default=True,
        ),
    ]
