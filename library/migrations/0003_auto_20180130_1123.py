# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-01-30 03:23
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('library', '0002_report'),
    ]

    operations = [
        migrations.CreateModel(
            name='DoMissionBackup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('executor', models.CharField(max_length=32)),
                ('issuer', models.CharField(max_length=32)),
                ('is_pass', models.IntegerField(default=0)),
                ('type', models.CharField(max_length=24)),
                ('description', models.TextField()),
                ('imageshot', models.ImageField(upload_to='imageshot/')),
                ('proof', models.ImageField(upload_to='proof/')),
                ('cost', models.IntegerField()),
                ('date_domission', models.DateTimeField()),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Mission')),
                ('missionlock', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.MissionLock')),
            ],
        ),
        migrations.CreateModel(
            name='DoMissionImageBackup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('proof', models.ImageField(upload_to='proof/')),
                ('date_domissionimage', models.DateTimeField()),
                ('domission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.DoMission')),
            ],
        ),
        migrations.CreateModel(
            name='MissionImageBackup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('imageshots', models.ImageField(upload_to='imageshot/')),
                ('date_missionimage', models.DateTimeField()),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Mission')),
            ],
        ),
        migrations.CreateModel(
            name='MissionLockBackup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('locker', models.CharField(max_length=32)),
                ('issuer', models.CharField(max_length=32)),
                ('is_pass', models.IntegerField(default=0)),
                ('type', models.CharField(max_length=24)),
                ('description', models.TextField()),
                ('imageshot', models.ImageField(upload_to='imageshot/')),
                ('cost', models.IntegerField()),
                ('date_lock', models.DateTimeField()),
                ('mission', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='library.Mission')),
            ],
        ),
        migrations.RemoveField(
            model_name='report',
            name='mission',
        ),
        migrations.DeleteModel(
            name='Report',
        ),
    ]
