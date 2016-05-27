from __future__ import unicode_literals
from django.db import models
from django.utils.translation import ugettext_lazy as _


class City(models.Model):
    name = models.CharField(max_length=40)
    corrected_name = models.CharField(max_length=40, null=True, blank=True)
    
    class Meta:
        ordering = ('name',)
        
    def __str__(self):
        return self.name
