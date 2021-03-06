# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-04-12 03:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('qac', '0006_comment'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='question',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='qac.Question'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='answer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='qac.Answer'),
        ),
    ]
