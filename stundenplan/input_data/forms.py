from django import forms
from stundenplan.models import *
from django_select2.forms import Select2Widget, Select2MultipleWidget

class ClassForm(forms.ModelForm):
    class Meta:
        model = Class 
        fields = ['name', 'schueleranzahl']
        widgets = {
            'name': forms.Select(attrs={'placeholder': 'Name eingeben...'}),
            'schueleranzahl': forms.NumberInput(attrs={'placeholder': 'Schüleranzahl eingeben...'})
        }
    

class GradeForm(forms.ModelForm):
    class Meta:
        model = Grade
        fields = ['name']
        widgets = {
            'name': forms.NumberInput(attrs={'placeholder': 'Klassenstufe eingeben...'})
        }


class SubjectGradeForm(forms.ModelForm):
    class Meta:
        model = Subject_Grade
        fields = ['subject', 'grade', 'wochenstunden']
        widgets = {
            'subject': Select2Widget(attrs={'placeholder': 'Fächer auswählen...'}),
            'wochenstunden': forms.NumberInput(attrs={'placeholder': 'Wochenstunden eingeben...'})
        }

class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['first_name', 'last_name', 'short_name', 'subjects']
        
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'Vorname eingeben...'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Nachname eingeben...'}),
            'short_name': forms.TextInput(attrs={'placeholder': 'Kürzel eingeben...'}),
            'subjects': Select2MultipleWidget(attrs={'placeholder': 'Fächer auswählen...'}),
        }

    #Fächer als Dropdown
class SubjectForm(forms.ModelForm):
    class Meta:
        model = Subject
        fields = ['abkuerzung', 'name']
        widgets = {
            'abkuerzung': forms.TextInput(attrs={'placeholder': 'Abkürzung eingeben...'}),
            'name': forms.TextInput(attrs={'placeholder': 'Fachname eingeben...'}),
        }

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ['room_number']
        widgets = {
            'room_number': forms.TextInput(attrs={'placeholder': 'Raumnummer eingeben...'}),
        }

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
    extra=0, 
    can_delete=True
)
SubjectGradeFormSet = forms.inlineformset_factory(
    Grade,
    Subject_Grade,
    form=SubjectGradeForm,
    extra=1,
    can_delete=True
)