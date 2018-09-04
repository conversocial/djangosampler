# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Query',
            fields=[
                ('hash', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('query', models.TextField()),
                ('total_duration', models.FloatField(default=0)),
                ('total_cost', models.FloatField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('query_type', models.CharField(max_length=32, db_index=True)),
                ('created_dt', models.DateTimeField(default=datetime.datetime.now, editable=False, db_index=True)),
            ],
            options={
                'verbose_name_plural': 'queries',
            },
        ),
        migrations.CreateModel(
            name='Sample',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('query', models.TextField()),
                ('duration', models.FloatField()),
                ('cost', models.FloatField()),
                ('params', models.TextField()),
                ('created_dt', models.DateTimeField(default=datetime.datetime.now, editable=False)),
            ],
        ),
        migrations.CreateModel(
            name='Stack',
            fields=[
                ('hash', models.CharField(max_length=32, serialize=False, primary_key=True)),
                ('stack', models.TextField()),
                ('total_duration', models.FloatField(default=0)),
                ('total_cost', models.FloatField(default=0)),
                ('count', models.IntegerField(default=0)),
                ('created_dt', models.DateTimeField(default=datetime.datetime.now, editable=False)),
                ('query', models.ForeignKey(to='djangosampler.Query')),
            ],
        ),
        migrations.AddField(
            model_name='sample',
            name='stack',
            field=models.ForeignKey(to='djangosampler.Stack'),
        ),
    ]
