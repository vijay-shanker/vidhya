from __future__ import unicode_literals
import datetime
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.conf import settings
# Create your models here.

class DownloadLimits(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    num_count = models.PositiveIntegerField(default=0)
    date = models.DateField(_('Date'), default=datetime.date.today)
    
    def __str__(self):
        return '{}-{}-{}'.format(self.user.email, self.num_count, self.date)

class Skill(models.Model):
    name = models.CharField(_('Skill'), max_length=255)
    
    class Meta:
        verbose_name_plural = 'Skills'
        ordering = ('name',)
        
    def __str__(self):
        return self.name
    

class Qualification(models.Model):
    '''
    A model to capture candidates qualifications
    '''
    
    COURSE_CHOICES = (
        ('PG','PG_Course'),
        ('UG', 'UG_Course'),
        ('POST_PG', 'Post_PG')
        )
    
    course_type = models.CharField(_('Course Type'), max_length=10, choices=COURSE_CHOICES)
    
    course_name = models.CharField(_('Course Name'), max_length=100)
    
    corrected_course_name = models.CharField(
        _('Corrected Course Name'), max_length=100, 
        null=True, blank=True)
    
    institute = models.CharField(_('Institute'), max_length=100, null=True, blank=True)
    
    tier1 = models.BooleanField(_('Is Tier1'), default=False)
    
    passing_year = models.CharField(
        _('Passing Year'), max_length=5, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Qualifications'
        ordering = ('course_name',)
        
    def __str__(self):
        return '{}-{}'.format(self.course_type, self.course_name)


class Candidate(models.Model):
    '''
    A model to hold candidate entries
    '''
    
    serial_no = models.PositiveIntegerField(_('Serial Number'))
    
    have_resume = models.BooleanField(_('Have Resume'), default=False)
    
    name= models.CharField(_('Name'), max_length=100)
    
    mobile_no = models.CharField(_('Mobile Number'), max_length=20)
    
    email = models.EmailField(_('Email'), max_length=254)
    
    qualifications = models.ManyToManyField(
        'candidate.Qualification', blank=True, 
        verbose_name=_('Qualifications'))
    
    skills = models.ManyToManyField(
        'candidate.Skill', blank=True, 
        verbose_name=_('Candidates Skillset'))
    
    work_exp = models.PositiveIntegerField(_('Work Experience'), default=0)
    
    analytics_exp = models.PositiveIntegerField(_('Analytics Experience'), default=0)
    
    current_city = models.ForeignKey(
        'core.City', null=True, blank=True, 
        related_name="current_city", verbose_name=_('Current city'))
    
    nearest_city = models.ForeignKey(
        'core.City', null=True, blank=True, 
        related_name="nearest_city", verbose_name=_('Nearest City'))
    
    preferred_city = models.ManyToManyField(
        'core.City', blank=True, related_name='preferred_city', verbose_name=_('Preferred cities'))
    
    ctc = models.FloatField(_('Current CTC'), default=0)
    
    current_employer = models.CharField(_('Current Employer'), max_length=255, null=True, blank=True)
    
    current_designation = models.CharField(max_length=255, null=True, blank=True)
    
    class Meta:
        verbose_name_plural = 'Candidates'
        ordering = ('name',)
    
    def __str__(self):
        return self.name
    
 