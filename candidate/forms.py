from django import forms
from .models import Candidate, Skill
from core.models import City


QCHOICES = (
    ('UG','Graduate'),
    ('PG', 'Postgraduate'),
    ('POST_PG', 'Post PG')
    )

WEXPCHOICES =(
    (0, '0-1'),
    (1, '1-2'),
    (2, '2-3'),
    (3, '3-4'),
    (4, '4-5'),
    (5, '5 and more'),
    ) 

CTC_CHOICES = (
    ('0-3', '0-3'),
    ('3-5', '3-5'),
    ('5-8', '5-8'),
    ('8', 'Above 8')
    )

class SearchForm(forms.Form):
    qualification = forms.ChoiceField(choices=QCHOICES, required=False)
    
    location = forms.ModelMultipleChoiceField(
        queryset=City.objects.all(), required=False)
    
    work_experience = forms.ChoiceField(choices=WEXPCHOICES, required=False)
    
    skills = forms.ModelMultipleChoiceField(
        queryset=Skill.objects.all(), required=False)
    
    ctc = forms.ChoiceField(choices=CTC_CHOICES, required=False)
