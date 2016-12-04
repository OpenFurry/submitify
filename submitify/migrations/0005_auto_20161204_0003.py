# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2016-12-04 00:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('submitify', '0004_auto_20161124_1926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='call',
            name='restricted_to',
            field=models.ManyToManyField(related_name='submitify_invitations', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='notification',
            name='call',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitify_notifications', to='submitify.Call'),
        ),
        migrations.AlterField(
            model_name='notification',
            name='targets',
            field=models.ManyToManyField(related_name='submitify_notifications', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='owner',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitify_reviews', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='review',
            name='submission',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitify_reviews', to='submitify.Submission'),
        ),
        migrations.AlterField(
            model_name='submission',
            name='call',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='submitify_submissions', to='submitify.Call'),
        ),
    ]
