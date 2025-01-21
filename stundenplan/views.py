from django.shortcuts import render
from stundenplan.models import Subject

def index(request):
  #Variablen in Stundenplan einfügen 
  monA1 = "Hallo"
  
  subjects = Subject.objects.all()
  return render(request, 'index.html', {'subjects': subjects, 'monA1': monA1})
