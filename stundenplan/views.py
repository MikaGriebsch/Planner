from django.shortcuts import render
from stundenplan.models import Subject

def index(request):
  #Variablen in Stundenplan einfügen 
  monA1 = "IF"
  monA1Name = "Wf"
  monA1Nr = "1.5"
  
  subjects = Subject.objects.all()
  return render(request, 'index.html', 
    {
    #first lesson
    'subjects': subjects, 
    'monA1': monA1, 
    'monA1Name': monA1Name, 
    'monA1Nr': monA1Nr
    #second lesson
    
    #third/fourth lesson
    
    #fifth/sixth lesson
    
    #seventh/eighth lesson
    })
