from django.shortcuts import render
from stundenplan.models import Subject

def index(request):
  subjects = Subject.objects.all()
  return render(request, 'index.html', {'subjects': subjects})

