from django.urls import path
from . import views

urlpatterns = [
    path('default/', views.default_view, name='default_view'),
    path('create/', views.input_view, name='input_view'),
    path('<str:klassenname>/', views.index_view, name='index_view'),
]



