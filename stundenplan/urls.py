from django.urls import path
from . import views
from django.urls import path, re_path

urlpatterns = [
    path('default/', views.default_view, name='default_view'),
    path('<str:bezeichnung>/', views.index_view, name='index_view'),

]



