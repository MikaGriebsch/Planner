from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
from .models import Mark
from .forms import MarkForm
from django.core.exceptions import ValidationError
from stundenplan.models import Subject, Class
from django.contrib import messages


def index_view(request):
    user_class = request.user.profile.klasse
    subjects_in_class = Subject.objects.filter(grade=user_class.grade).distinct()
    marks = Mark.objects.filter(user=request.user, subject__in=subjects_in_class)

    return render(request, 'tabelle.html', {'marks': marks, 'subjects_in_class': subjects_in_class})

@require_POST
def save_marks(request):
    user_class = request.user.profile.klasse
    subjects_in_class = Subject.objects.filter(grade=user_class.grade).distinct()

    for subject in subjects_in_class:
        mark = Mark.objects.filter(user=request.user, subject=subject).first()
        if not mark:
            mark = Mark(user=request.user, subject=subject)

        for i in range(1, 11):
            field_name = f"note_{i}_{mark.id}"
            if field_name in request.POST:
                value = request.POST[field_name]
                setattr(mark, f"note_{i}", int(value) if value else None)

        klausur_field_name = f"klausur_{mark.id}"
        if klausur_field_name in request.POST:
            value = request.POST[klausur_field_name]
            mark.klausur = int(value) if value else None

        mark.save()
    return redirect('index_view')