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


class SubjectGradeForm(forms.ModelForm):
    class Meta:
        model = Subject_Grade
        fields = ['subject', 'grade', 'wochenstunden']
        widgets = {
            'subject': Select2Widget()
        }

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
        fields = ['abkuerzung', 'name']

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number']

TeacherFormSet = forms.modelformset_factory(
    Teacher, 
    form=TeacherForm,
    extra=1, 
    can_delete=True
)
SubjectFormSet = forms.modelformset_factory(
    Subject, 
    form=SubjectForm, 
    extra=1, 
    can_delete=True
)
RoomFormSet = forms.modelformset_factory(
    Room,
    form=RoomForm,
    extra=1,
    can_delete=True
)
GradeFormSet = forms.modelformset_factory(
    Grade, 
    form=GradeForm, 
    extra=0, 
    can_delete=True
)
ClassFormSet = forms.inlineformset_factory(
    Grade, 
    Class, 
    form=ClassForm, 
    extra=1, 
    can_delete=True
)
SubjectGradeFormSet = forms.inlineformset_factory(
    Grade,
    Subject_Grade,
    form=SubjectGradeForm,
    extra=0,
    can_delete=True
)