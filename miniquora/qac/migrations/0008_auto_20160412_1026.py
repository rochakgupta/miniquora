# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-12 04:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qac', '0007_auto_20160412_0926'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='answer',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='qac.Answer'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='question',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='qac.Question'),
        ),
    ]
