# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('supplified', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MasterImportUpload',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('file_name', models.CharField(max_length=500)),
                ('process_name', models.CharField(max_length=300)),
                ('process_type', models.CharField(max_length=50)),
                ('uploaded_on', models.DateTimeField(auto_now=True)),
                ('applied_on', models.DateTimeField(null=True, blank=True)),
                ('query', models.TextField(null=True, blank=True)),
                ('error', models.TextField(null=True, blank=True)),
                ('applied', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
