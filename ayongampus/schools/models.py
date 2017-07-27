from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class School(models.Model):
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=140)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return self.name


class Student(models.Model):
    user = models.ForeignKey(User, related_name='+')
    identity_number = models.BigIntegerField()
    school = models.ForeignKey(School)
    is_graduated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return unicode(self.identity_number)


class Teacher(models.Model):
    user = models.ForeignKey(User, related_name='+')
    school = models.ForeignKey(School)
    identity_number = models.BigIntegerField()
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __unicode__(self):
        return unicode(self.identity_number)
