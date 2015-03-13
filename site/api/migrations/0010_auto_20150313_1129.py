# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_load_pos_fixture_data'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='url',
        ),
        migrations.RemoveField(
            model_name='page',
            name='url',
        ),
        migrations.AddField(
            model_name='document',
            name='external_url',
            field=models.CharField(max_length=128, null=True, db_column=b'url'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='page',
            name='identifier',
            field=models.URLField(null=True, db_column=b'url'),
            preserve_default=True,
        ),
    ]
