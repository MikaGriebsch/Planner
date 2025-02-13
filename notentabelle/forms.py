from django import forms
from .models import Mark
from .models import Semester_Marks
from stundenplan.models import Subject

class MarkForm(forms.ModelForm):
    class Meta:
        model = Mark
        fields = ['note_1', 'note_2', 'note_3', 'note_4', 'note_5', 'note_6', 'note_7', 'note_8', 'note_9', 'note_10', 'klausur', 'subject']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            user_class = user.profile.klasse
            self.fields['subject'].queryset = Subject.objects.filter(grade=user_class.grade)

class SemesterMarksForm(forms.ModelForm):
    class Meta:
        model = Semester_Marks
        fields = ['semester_1', 'semester_2', 'semester_3', 'semester_4', 'subject']

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            user_class = user.profile.klasse
            self.fields['subject'].queryset = Subject.objects.filter(grade=user_class.grade)