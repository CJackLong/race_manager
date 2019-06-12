from django.urls import path
from . import views

urlpatterns = [
    path('', views.calendar, name='calendar'),

    path('races/',views.races, name='races'),

    path('races/<race_name>/', views.race_detail, name='race_detail'),

    path('athletes/', views.athletes, name='athletes'),

    path('athlete_detail/<ustsa_num>/', views.athlete_detail, name='athlete_detail'),

]
