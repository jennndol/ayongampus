from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Follow(models.Model):
    user = models.ForeignKey(User, related_name="who_is_following")
    following = models.ForeignKey(User, related_name="who_is_followed")
    created_date = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return unicode(self.id)

    def get_absolute_url(self):
        return "/friends/%s/" % (self.slug)
