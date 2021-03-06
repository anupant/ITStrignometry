# -*- coding: utf-8 -*-
# Generated by Django 1.9.4 on 2017-06-14 05:30
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('learning', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Question1',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_title', models.CharField(max_length=250)),
                ('question_description', models.FileField(upload_to=b'')),
                ('question_option1', models.CharField(max_length=250)),
                ('question_option2', models.CharField(max_length=250)),
                ('question_option3', models.CharField(max_length=250)),
                ('question_option4', models.CharField(max_length=250)),
                ('question_hint1', models.CharField(max_length=250)),
                ('question_no', models.IntegerField()),
                ('question_right_answer', models.CharField(max_length=250)),
                ('question_explanation', models.CharField(max_length=250)),
                ('question_difficulty', models.CharField(max_length=250)),
                ('hint_taken', models.BooleanField(default=False)),
                ('quiz', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='learning.Quiz')),
            ],
        ),
    ]
