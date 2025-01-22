from django.shortcuts import render
from stundenplan.models import Subject
from django.http import HttpResponse

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

def test_view(request, klassenname):
    test_inhalte = {
      "7a": "Dies ist die Seite für Klasse 7a.",
      "7b": "Willkommen in Klasse 7b.",
      "8a": "Hier findest du Infos zu Klasse 8a.",
    }

    # Überprüfen, ob die Klasse existiert
    if klassenname in test_inhalte:
      inhalt = test_inhalte[klassenname]
    else:
      inhalt = "Diese Klasse existiert nicht."

    return HttpResponse(inhalt)
