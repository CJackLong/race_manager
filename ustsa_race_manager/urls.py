from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),

    path('races/',views.races, name='races'),

    path('races/<race_id>/', views.race_detail, name='race_detail'),

    path('athletes/', views.athletes, name='athletes'),

    path('athlete_detail/<athlete_id>/', views.athlete_detail, name='athlete_detail'),

]
