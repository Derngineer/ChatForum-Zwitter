from django.urls import path
from . import views

urlpatterns = [
path('',views.home, name= 'home'),
path('profiles/',views.profile_list, name ='profile_list'),
path('profile/<int:pk>',views.profile, name = 'profile'),
path('registration/',views.registration, name ='registration'),
path('sign_in/',views.sign_in , name = 'sign_in'),
]