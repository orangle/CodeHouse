# coding:utf-8
from __future__ import unicode_literals

from django.db import models

class Todo(models.Model):

    text = models.CharField(max_length=200)
    addtime = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return 'Todo:{0}'.format(self.text)
