from __future__ import unicode_literals
from django.conf import settings
from django.db import models

# Create your models here.
class UploadCandidatesData(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    upload = models.FileField(upload_to='uploads/%Y/%m/%d/')
    
    def __str__(self):
        return 'uploaded by: {}'.format(self.user.email)
