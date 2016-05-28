from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import PermissionsMixin
from django.utils import timezone

class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('Male','Male'),
        ('Female','Female')
    )
            
    email = models.EmailField(_('Email'),unique=True)
    
    username = models.CharField(_('User Name'),max_length=100, null=True)
    
    contact_no = models.CharField(
        _('Contact Number'),max_length=20, 
        null=True, blank=True)
    
    gender = models.CharField(
        _('Gender'),max_length=10, null=True, 
        blank=True, choices=GENDER_CHOICES )
    
    is_staff = models.BooleanField(
        _('Staff status'), default=False,
        help_text=_('whether the user can log into this admin '
                    'site.'))
    
    is_active = models.BooleanField(
        _('Active'), default=True,
        help_text=_('Designates whether this user should be treated as '
                    'active. Unselect this instead of deleting accounts.'))

    date_joined = models.DateTimeField(_('date joined'),default=timezone.now)
    
    USERNAME_FIELD='email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()
    
    def __unicode__(self):
        return "%s" % self.email
    
    def get_short_name(self):
        return self.username
    
    def save(self, *args, **kwargs):
        if not self.pk or self.has_usable_password()==False:
            self.set_password(self.password)
        super(User, self).save(*args, **kwargs)
    