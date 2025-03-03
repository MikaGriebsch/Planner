from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from stundenplan import get_plan
from django.shortcuts import render
from .get_plan import get_plan
from django.http import HttpResponse
from .input_data.forms import ClassForm, GradeForm


@login_required
def index_view(request, bezeichnung):
    
    user = request.user

    if request.user.is_superuser or request.user.profile.klasse.bezeichnung == bezeichnung:
        context = get_plan(user, bezeichnung)
        return render(request, 'index.html', context)

def default_view(request):
    return render(request, 'default.html')

#@login_required
def input_view(request):
    class_form = ClassForm()
    grade_form = GradeForm()
    return render(request,'input.html', {'class_form': class_form, 'grade_form': grade_form})
