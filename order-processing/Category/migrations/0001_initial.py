# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
            ],
            options={
                'db_table': 'category',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
