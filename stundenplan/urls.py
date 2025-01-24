from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView
from .views import register
from django.contrib.auth.views import LogoutView
from .views import register, CustomLoginView

urlpatterns = [
    path('default/', views.default_view, name='default_view'),
    path('planner/<str:klassenname>/', views.index_view, name='index_view'),
    path('', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('register/', views.register, name='register'),
]



