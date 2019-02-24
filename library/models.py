#!/usr/bin/env python
# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Mission(models.Model):
    user = models.CharField(max_length=32, unique=False)
    type = models.CharField(max_length=24)
    description = models.TextField()
    imageshot = models.ImageField(upload_to='imageshot/')
    capital = models.IntegerField()
    cost = models.IntegerField()
    amount = models.IntegerField()
    totalcost = models.IntegerField()
    date_mission = models.DateTimeField()

    def __unicode__(self):
        return '%s' % (self.user)

    def toJSON(self):
        fields = []
        for field in self._meta.fields:
            fields.append(field.name)

        d = {}
        for attr in fields:
            d[attr] = getattr(self, attr)

        import json
        return json.dumps(d)


class MissionBackup(models.Model):
    user = models.CharField(max_length=32, unique=False)
    type = models.CharField(max_length=24)
    description = models.TextField()
    imageshot = models.ImageField(upload_to='imageshot/')
    capital = models.IntegerField()
    cost = models.IntegerField()
    amount = models.IntegerField()
    totalcost = models.IntegerField()
    date_mission = models.DateTimeField()


class MissionImage(models.Model):
    mission = models.ForeignKey(Mission)
    imageshots = models.ImageField(upload_to='imageshot/')
    date_missionimage = models.DateTimeField()


class MissionImageBackup(models.Model):
    mission = models.ForeignKey(Mission)
    imageshots = models.ImageField(upload_to='imageshot/')
    date_missionimage = models.DateTimeField()


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=16, unique=True)
    phone = models.CharField(max_length=32, unique=True)
    email = models.EmailField(unique=True)
    photo = models.ImageField(upload_to='portrait/')
    integral = models.IntegerField(default=1000)


class MissionLock(models.Model):
    mission = models.ForeignKey(Mission)
    locker = models.CharField(max_length=32, unique=False)
    issuer = models.CharField(max_length=32)
    is_pass = models.IntegerField(default=0)
    type = models.CharField(max_length=24)
    description = models.TextField()
    imageshot = models.ImageField(upload_to='imageshot/')
    cost = models.IntegerField()
    date_lock = models.DateTimeField()


class MissionLockBackup(models.Model):
    mission = models.ForeignKey(Mission)
    locker = models.CharField(max_length=32, unique=False)
    issuer = models.CharField(max_length=32)
    is_pass = models.IntegerField(default=0)
    type = models.CharField(max_length=24)
    description = models.TextField()
    imageshot = models.ImageField(upload_to='imageshot/')
    cost = models.IntegerField()
    date_lock = models.DateTimeField()


class DoMission(models.Model):
    missionlock = models.ForeignKey(MissionLock)
    mission = models.ForeignKey(Mission)
    executor = models.CharField(max_length=32)
    issuer = models.CharField(max_length=32)
    is_pass = models.IntegerField(default=0)
    type = models.CharField(max_length=24)
    description = models.TextField()
    imageshot = models.ImageField(upload_to='imageshot/')
    proof = models.ImageField(upload_to='proof/')
    cost = models.IntegerField()
    date_domission = models.DateTimeField()


class DoMissionBackup(models.Model):
    missionlock = models.ForeignKey(MissionLock)
    mission = models.ForeignKey(Mission)
    executor = models.CharField(max_length=32)
    issuer = models.CharField(max_length=32)
    is_pass = models.IntegerField(default=0)
    type = models.CharField(max_length=24)
    description = models.TextField()
    imageshot = models.ImageField(upload_to='imageshot/')
    proof = models.ImageField(upload_to='proof/')
    cost = models.IntegerField()
    date_domission = models.DateTimeField()


class DoMissionImage(models.Model):
    domission = models.ForeignKey(DoMission)
    proof = models.ImageField(upload_to='proof/')
    date_domissionimage = models.DateTimeField()


class DoMissionImageBackup(models.Model):
    domission = models.ForeignKey(DoMission)
    proof = models.ImageField(upload_to='proof/')
    date_domissionimage = models.DateTimeField()


