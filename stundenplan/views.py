from django.shortcuts import render
from stundenplan.models import Name

def index(request):
    #context = {
     #   'name': 'Mika',
      #  'class': '7A'
    #}
    names = Name.objects.all()
    return render(request, 'index.html', {'names': names})

