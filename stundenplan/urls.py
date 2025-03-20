from django.urls import path
from . import views

urlpatterns = [
    path('default/', views.default_view, name='default_view'),
    path('create/', views.input_view, name='input_view'),
	path('create/save/', views.save_input, name='save_input'),
    path('<str:bezeichnung>/', views.index_view, name='index_view'),
]



