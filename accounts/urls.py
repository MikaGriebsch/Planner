from django.urls import path
from . import views
from .views import CustomLoginView
from django.contrib.auth.views import LogoutView
from django.views.generic import RedirectView

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('first_login/', views.first_login, name='first_login'),
    path('', RedirectView.as_view(url='login/')),
    path('changePassword/', views.change_password, name='change_password'),
]