# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoodsInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('gtitle', models.CharField(max_length=10)),
                ('gpic', models.ImageField(upload_to=b'goods')),
                ('gprice', models.DecimalField(max_digits=5, decimal_places=2)),
                ('gunit', models.CharField(default=b'500g', max_length=20)),
                ('gclick', models.IntegerField()),
                ('gintro', models.CharField(max_length=300)),
                ('gstore', models.IntegerField()),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='TypeInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ttitle', models.CharField(max_length=20)),
                ('isDelete', models.BooleanField(default=False)),
            ],
        ),
        migrations.AddField(
            model_name='goodsinfo',
            name='gtype',
            field=models.ForeignKey(to='agoods.TypeInfo'),
        ),
    ]
