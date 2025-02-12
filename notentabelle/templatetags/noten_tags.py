from django import template

register = template.Library()

@register.filter
def get_mark_for_subject(marks, subject):
    return marks.filter(subject=subject).first()