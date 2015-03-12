# -*- coding: utf-8 -*-
from django.db import models, migrations
from django.core.management import call_command

app_name = 'api'
fixture = model_name = 'PartOfSpeech'


def load_fixture(apps, schema_editor):
    call_command('loaddata', fixture, app_label=app_name)


def unload_fixture(apps, schema_editor):
    "Deleting all entries for this model"

    PartOfSpeech = apps.get_model(app_name, model_name)
    PartOfSpeech.objects.all().delete()


class Migration(migrations.Migration):
    dependencies = [
        (app_name, '0008_posmention'),
     ]

    operations = [
        migrations.RunPython(load_fixture, reverse_code=unload_fixture),
    ]
