from django.shortcuts import render
from stundenplan.models import Subject, Class
from django.http import HttpResponse


def index_view(request, klassenname):
  monA1 = "IF"
  monA1Name = "Wf"
  monA1Nr = "1.5"

  subjects = Subject.objects.all()
  
  if Class.objects.filter(name=klassenname).exists():
    return render(request, 'index.html', 
    {
      #class name
      'klassenname': klassenname,

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

def default_view(request):
  return render(request, 'default.html')
