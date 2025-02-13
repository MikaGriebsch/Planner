from django import template
from ..models import Mark, Semester_Marks

register = template.Library()

@register.filter
def get_mark_for_subject(marks, subject):
    return marks.filter(subject=subject).first()

@register.filter
def get_semester_marks_for_subject(semester_marks, subject):
    return semester_marks.filter(subject=subject).first()