from django.urls import path
from . import views

urlpatterns = [
    path('default/', views.default_view, name='default_view'),
    path('create/', views.input_view, name='input_view'),
	path('create/save/', views.save_input, name='save_input'),
	path('create/save-subject/', views.save_subject, name='save_subject'),
    path('create/get-subjects/', views.get_subjects, name='get_subjects'),
	path('create/delete-subject/', views.delete_subject, name='delete_subject'),
    path('<str:bezeichnung>/', views.index_view, name='index_view'),
]



