# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-11-24 00:55
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('submitify', '0002_call_invite_only'),
    ]

    operations = [
        migrations.RenameField(
            model_name='guideline',
            old_name='value',
            new_name='value_raw',
        ),
        migrations.AddField(
            model_name='guideline',
            name='value_rendered',
            field=models.TextField(default=' '),
            preserve_default=False,
        ),
    ]
