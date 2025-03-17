from django import forms
from stundenplan.models import *
from django_select2.forms import Select2Widget, Select2MultipleWidget

class BaseForm(forms.Form):
   #wrappper für alle forms
   platzhalter = 0

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class 
        fields = ['name', 'schueleranzahl']

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['name']

    #subject grade connection

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'short_name', 'subjects']
        
        widgets = {
            'subjects': Select2MultipleWidget()
        }

    #Fächer als Dropdown
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['abkuerzung', 'name', 'grade']



# liber mit standardform  und dann einfach rooms als list input angeben
class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number']

TeacherFormSet = forms.modelformset_factory(Teacher, form=TeacherForm, extra=1, can_delete=True)