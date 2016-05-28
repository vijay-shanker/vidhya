from django.contrib import admin
from .models import UploadCandidatesData
from .forms import CandidateDataForm

class UploadCandidatesDataAdmin(admin.ModelAdmin):
    model = UploadCandidatesData
    form = CandidateDataForm
    
admin.site.register(UploadCandidatesData, UploadCandidatesDataAdmin)
