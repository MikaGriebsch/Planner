from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('test/<str:klassenname>/', views.test_view, name='test_view'),
    
]
