# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('uname', models.CharField(max_length=20)),
                ('upasswd', models.CharField(max_length=40)),
                ('uemail', models.CharField(default=b'', max_length=40)),
                ('ushou', models.CharField(default=b'', max_length=30)),
                ('uaddress', models.CharField(default=b'', max_length=200)),
                ('uyoubian', models.CharField(default=b'', max_length=6)),
                ('uphone', models.CharField(default=b'', max_length=11)),
            ],
        ),
    ]
