import openpyxl as px
from django import forms
from .models import UploadCandidatesData
from core.utils import UploadData

class CandidateDataForm(forms.ModelForm):
    class Meta:
        model = UploadCandidatesData
        exclude = ()
        
    def clean_upload(self):
        xlfile = self.cleaned_data['upload']
        W = px.load_workbook(xlfile, use_iterators = True)
        p = W.get_sheet_by_name(name = 'Sheet1')

        data_list = []
        column_map = self.get_column_keys()
        for row in p.iter_rows(row_offset=1):
            mydict = {}
            for i in row:
                if i.column:
                    mydict[column_map[str(i.column)]] = i.value
            data_list.append(mydict)
        
        upload_data = UploadData(data_list)
        upload_data.create_candidates()
        return xlfile
    
    def get_column_keys(self):
        '''
        mapping of xl-sheet header to field names/other name
        '''
        
        return {
            '1': 'serial_no',
            '2': 'have_resume',
            '3': 'name',
            '4': 'mobile_no',
            '5': 'email',
            '6': 'work_exp',
            '7': 'analytics_exp',
            '8': 'current_city',
            '9': 'corrected_city_name',
            '10': 'nearest_city',
            '11': 'preferred_city',
            '12': 'ctc',
            '13': 'current_employer',
            '14': 'current_designation',
            '15': 'skills',
            '16': 'UG_Course',
            '17': 'corrected_ug_course_name',
            '18': 'UG_institute',
            '19': 'UG_tier1',
            '20': 'UG_passing_year',
            '21': 'PG_Course',
            '22': 'corrected_pg_course_name',
            '23': 'PG_institute',
            '24': 'PG_tier1',
            '25': 'PG_passing_year',
            '26': 'Post_PG',
            '27': 'corrected_post_pg_course_name'
            }
        
        
        