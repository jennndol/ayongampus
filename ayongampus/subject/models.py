from __future__ import unicode_literals

import re

from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils.encoding import python_2_unicode_compatible
from django.utils.translation import ugettext as _


def get_subject_by_subject_name(subject):
    return Subject.objects.get(subject=subject)


def get_subject_by_id(id):
    return Subject.objects.get(pk=id)


class SubjectManager(models.Manager):
    def new_subject(self, subject):
        new_subject = self.create(subject=re.sub('\s+', '-', subject)
                                  .lower())

        new_subject.save()
        return new_subject


@python_2_unicode_compatible
class Subject(models.Model):
    subject = models.CharField(verbose_name=_("Subject"), max_length=250, unique=True)

    author = models.ForeignKey(User, null=True)

    objects = SubjectManager()

    class Meta:
        verbose_name = _("Subject")
        verbose_name_plural = _("Subjects")

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse('core_subject_detail', kwargs={'pk': self.pk})

@python_2_unicode_compatible
class Chapter(models.Model):
    chapter = models.CharField(
        verbose_name=_("Chapter"),
        max_length=250, blank=True, null=True)

    subject = models.ForeignKey(
        Subject, null=True, blank=True,
        verbose_name=_("Subject"))

    objects = SubjectManager()

    class Meta:
        verbose_name = _("Chapter")
        verbose_name_plural = _("Chapters")

    def __str__(self):
        return self.chapter + " (" + self.subject.subject + ")"
