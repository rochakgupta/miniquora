# -*- coding: utf-8 -*-
# Generated by Django 1.9.2 on 2016-03-31 14:41
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('qac', '0003_answer_comment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='comment',
            name='answer',
        ),
    ]
