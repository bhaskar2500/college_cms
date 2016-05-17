# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations

class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AdminFunctions',
            fields=[
            ],
            options={
                'db_table': 'admin_functions',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='AdminUser',
            fields=[
            ],
            options={
                'db_table': 'admin_user',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Attribute',
            fields=[
            ],
            options={
                'db_table': 'attribute',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Banners',
            fields=[
            ],
            options={
                'db_table': 'banners',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CartValue',
            fields=[
            ],
            options={
                'db_table': 'cart_value',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Category2',
            fields=[
            ],
            options={
                'db_table': 'category2',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryShippingCharge',
            fields=[
            ],
            options={
                'db_table': 'category_shipping_charge',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CatSolrBackLog',
            fields=[
            ],
            options={
                'db_table': 'cat_solr_back_log',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='DjangoMigrations',
            fields=[
            ],
            options={
                'db_table': 'django_migrations',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FilterProductMapping',
            fields=[
            ],
            options={
                'db_table': 'filter_product_mapping',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Filters',
            fields=[
            ],
            options={
                'db_table': 'filters',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='FinalTable',
            fields=[
            ],
            options={
                'db_table': 'final_table',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Logging',
            fields=[
            ],
            options={
                'db_table': 'logging',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Media',
            fields=[
            ],
            options={
                'db_table': 'media',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Mycart',
            fields=[
            ],
            options={
                'db_table': 'mycart',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
            ],
            options={
                'db_table': 'newsletter',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewsletterSubEmailid',
            fields=[
            ],
            options={
                'db_table': 'newsletter_sub_emailid',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='OrderInvoice',
            fields=[
            ],
            options={
                'db_table': 'order_invoice',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PincodeMaster',
            fields=[
            ],
            options={
                'db_table': 'pincode_master',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Pincodes',
            fields=[
            ],
            options={
                'db_table': 'pincodes',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Responsibilities',
            fields=[
            ],
            options={
                'db_table': 'responsibilities',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Sessions',
            fields=[
            ],
            options={
                'db_table': 'sessions',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SolrBackLog',
            fields=[
            ],
            options={
                'db_table': 'solr_back_log',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SyncLog',
            fields=[
            ],
            options={
                'db_table': 'sync_log',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TaxMaster',
            fields=[
            ],
            options={
                'db_table': 'tax_master',
                'managed': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='TempProductList',
            fields=[
            ],
            options={
                'db_table': 'temp_product_list',
                'managed': False,
            },
            bases=(models.Model,),
        ),
    ]
