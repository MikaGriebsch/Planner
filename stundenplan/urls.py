from django.urls import path
from . import views

urlpatterns = [
    path('<str:klassenname>/', views.index_view, name='index_view'),
    
]
