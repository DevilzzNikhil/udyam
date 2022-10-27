from django import views
from django.urls import path
from authentication.views import *

urlpatterns = [
    path('', home, name='home'),
    path('login/', login, name = 'login'),
    path('register/', register, name='register'),
    path('signout/', signout,  name='signout'),
    
]

