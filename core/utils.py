from django.db.models import Q
from core.models import *
from candidate.models import *

from functools import wraps
from django.core.exceptions import PermissionDenied

def recruiter_check(func):
    @wraps(func)
    def wrapper(request, *args, **kwargs):
        if any([ request.user.is_anonymous(), request.user.is_recruiter == False ]):
            if request.user.is_superuser:
                return func(request, *args, **kwargs)
            else:
                raise PermissionDenied
        else:
            return func(request, *args, **kwargs)
    return wrapper
    

class UploadData(object):
    '''
    This class receives a dict, and creates candidates with uploaded data.
    It can be used directly or can be called in task.
    '''
    
    def __init__(self, data):
        self.data = data
    
    def create_candidates(self):
        '''
        Used as entry point for this class,
        creates candidate and stores qualification/cities on that candidate
        '''
        
        for row in self.data:
            cdata = {}
            cdata['serial_no'] = row.get('serial_no', 0)
            cdata['have_resume'] = False if row.get('have_resume', 'No') == 'No' else True
            cdata['name'] = row.get('name','dummy')
            cdata['mobile_no'] = row.get('mobile_no', 'No contact No')
            cdata['email'] = row.get('email', 'dummy@dummy.com')
            cdata['work_exp'] = row.get('work_exp', 0)
            cdata['analytics_exp'] = row.get('analytics_exp', 0)
            cdata['ctc'] = row.get('ctc', 0.0)
            cdata['current_employer'] = row.get('current_employer', 'N/A')
            cdata['current_designation'] = row.get('current_designation', 'N/A')
            
            candidate, created = Candidate.objects.get_or_create(**cdata)
            
            self.set_city_related_data(candidate, row)
            self.set_qualifications(candidate, row)
            self.set_skills(candidate, row)
    
    def set_city_related_data(self, candidate, row):
        '''
        Maps city specific data to candidate
        '''
        nearest_city = row.get('nearest_city')
        current_city = row.get('current_city', 'N/A')
        corrected_name = row.get('corrected_city_name', '')
        
        if corrected_name:
            current_city = self.get_city(current_city, corrected_name)
        else:
            current_city = self.get_city(current_city, corrected_name=None)
        
        candidate.current_city = current_city
        
        
        nearest_city = self.get_city(nearest_city, corrected_name=None)
        candidate.nearest_city = nearest_city
        
        candidate.save()
        
        preferred_cities = row.get('preferred_city', '')
        preferred_cities = [each.strip() for each in preferred_cities.split(',')]
        if len(preferred_cities) == 1 and bool(preferred_cities[0]):
            city = self.get_city(preferred_cities[0], corrected_name=None)
            candidate.preferred_city.add(city)
        else:
            for cname in preferred_cities:
                city = self.get_city(cname, corrected_name=None)
                candidate.preferred_city.add(city)
            
    
    def get_city(self, city_name, corrected_name=None):
        '''
        utility function to get city, looks for __iexact match of city,
        in case of no match, creates the city and return 
        '''
        city_name = city_name.strip()
        
        if corrected_name:
            corrected_name = corrected_name.strip()
        
        try:
            if corrected_name:
                city = City.objects.get(
                    Q(name__iexact=city_name)|Q(corrected_name__iexact=corrected_name))
            else:
                city = City.objects.get(Q(name__iexact=city_name)|Q(corrected_name__iexact=city_name))
        except:
            if corrected_name:
                city = City.objects.create(
                    name=city_name, corrected_name=corrected_name)
            else:
                city = City.objects.create(name=city_name)
        
        return city
        
    def set_qualifications(self, candidate, row):
        '''
        Maps qualification to candidates,
        basically storing UG/PG/Post PG data
        '''
        
        if row.get('UG_Course', False):
            ug = {}
            ug['course_type'] = 'UG_Course'
            ug['course_name'] = row.get('UG_Course')
            ug['corrected_course_name'] = row.get('corrected_ug_course_name', '')
            ug['institute'] = row.get('UG_institute', '')
            ug['tier1'] = True if row.get('UG_tier1', False) == True else False
            ug['passing_year'] = row.get('UG_passing_year')
            qualification, created = Qualification.objects.get_or_create(**ug)
            candidate.qualifications.add(qualification)
        
        if row.get('PG_Course', False):
            pg ={}
            pg['course_type'] = 'PG_Course'
            pg['course_name'] = row.get('PG_Course')
            pg['corrected_course_name'] = row.get('corrected_pg_course_name', '')
            pg['institute'] = row.get('PG_institute', '')
            pg['tier1'] = True if row.get('PG_tier1', False) == True else False
            pg['passing_year'] = row.get('PG_passing_year')
            qualification, created = Qualification.objects.get_or_create(**pg)
            candidate.qualifications.add(qualification)
        
        if row.get('Post_PG', False):
            postpg ={}
            postpg['course_type'] = 'Post_PG'
            postpg['corrected_course_name'] = row.get('corrected_post_pg_course_name', '')
            qualification, created = Qualification.objects.get_or_create(**postpg)
            candidate.qualifications.add(qualification)
    
    def set_skills(self, candidate, row):
        '''
        Maps skills to candidates
        '''
        skills = row.get('skills', '')
        if skills:
            skills = [each.strip() for each in row.get('skills').split(',')]
            for skill in skills:
                skill, flag = Skill.objects.get_or_create(
                    name__iexact=skill, defaults={'name':skill})
                candidate.skills.add(skill)
    
    

        
              
            