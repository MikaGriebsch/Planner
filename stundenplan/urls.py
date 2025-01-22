from django.urls import path
from . import views

urlpatterns = [
    path('', views.default_view, name='default_view'),
    path('<str:klassenname>/', views.index_view, name='index_view'),
    
]
