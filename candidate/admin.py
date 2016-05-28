from django.contrib import admin
from .models import Candidate, Qualification, Skill

admin.site.register([Candidate, Qualification, Skill])
