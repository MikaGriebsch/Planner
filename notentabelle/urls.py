from django.urls import path
from .views import index_view, save_marks

urlpatterns = [
    path('', index_view, name='index_view'),
    path('save_marks/', save_marks, name='save_marks'),
]