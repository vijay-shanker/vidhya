import csv
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied

from .forms import SearchForm
from .models import Candidate
from core.utils import recruiter_check


class LoginView(TemplateView):
    template_name = 'signin.html'
    
    def post(self, request, *args, **kwargs):
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if not user:
            raise PermissionDenied
            
        login(request, user)
        
        if user.is_superuser:
            return redirect('/admin/')
        else:
            return redirect('/search/')
            

class SearchCandidates(TemplateView):
    template_name= 'search.html'
    form_class = SearchForm
    
    @method_decorator(recruiter_check)
    def dispatch(self, request, *args, **kwargs):
        return super(SearchCandidates, self).dispatch(request, *args, **kwargs)
    
    def get_context_data(self, *args, **kwargs):
        ctx = super(SearchCandidates, self).get_context_data(*args, **kwargs)
        ctx['form'] = self.form_class(self.request.GET)
        ctx['candidate_list'] = self.get_queryset()
        return ctx
    
    def get_queryset(self):
        queryset = Candidate.objects.all()
        return self.apply_search(queryset)
    
    def apply_search(self, queryset):
        '''
        Apply search with selected parameters
        '''
        
        if self.form_class(self.request.GET).is_valid():
            search_params = self.request.GET.copy()
        
        if all(['work_experience' in search_params, search_params.get('work_experience', False)]):
            lower_range = int(search_params['work_experience'])
            if lower_range == 5:
                queryset = queryset.filter(work_exp__gte=lower_range)
            else:
                queryset = queryset.filter(work_exp__range=(lower_range, lower_range+1))
        
        if all(['qualification' in search_params, search_params.get('qualification', False)]):
            queryset = queryset.filter(qualifications__course_type=search_params.get('qualification'))
        
        if all(['location' in search_params, search_params.getlist('location')]):
            queryset = queryset.filter(current_city_id__in=search_params.getlist('location'))
            
        if all(['skills' in search_params, search_params.getlist('skills')]):
            queryset = queryset.filter(skills__in=search_params.getlist('skills'))
        
        if 'ctc' in search_params:
            ctc = search_params.get('ctc')
            if ctc == '8':
                queryset = queryset.filter(ctc__gte=8)
            else:
                LR, UR = [int(each) for each in ctc.split('-')]
                queryset = queryset.filter(ctc__range=(LR,UR))
 
        return queryset
    
    def post(self, request, *args, **kwargs):
        '''
        post is called to get csv of filtered queryset
        '''
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment;filename="candidate_export.csv"'
        writer = csv.writer(response)
        writer.writerow([
            'Id', 'Serial No', 'name', 'mobile_no', 'qualification',
            'work experience', 'analytics exp', 'current city',
            'CTC', 'Current Designation', 'Current Employer'
            ])
        
        if not self.request.GET:
            queryset = Candidate.objects.all()
        else:
            queryset = self.apply_search(Candidate.objects.all())

        for c in queryset:
            writer.writerow([c.id, c.serial_no, c.name, c.mobile_no,
                ', '.join([q.course_name for q in c.qualifications.all()]),
                c.work_exp, c.analytics_exp, c.current_city.name,
                c.ctc, c.current_designation, c.current_employer])
        return response
         


