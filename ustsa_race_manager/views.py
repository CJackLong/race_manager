from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import Race, Racer, RacerResult

# Create your views here.
def index(request):

    num_races = Race.objects.all().count()
    num_racers = Racer.objects.all().count()


    recent_races = Race.objects.order_by('race_date')[:5]

    context = {
        'recent_races': recent_races,
        'num_races':num_races,
        'num_racers': num_racers
    }

    return render(request, 'ustsa_race_manager/index.html', context)

def race_detail(request, race_id):
    race = get_object_or_404(Race, pk=race_id)
    print(str(race.officials))

    race_results = RacerResult.objects.filter(race=race_id)

    for e in race_results:
        print(str(e.race))
    #race_results = get_object_or_404(RacerResult, fk=race_id)
    return render(request, 'ustsa_race_manager/race_detail.html', {'race': race, 'race_results': race_results})


def races(request):
    past_races = Race.objects.all()
    return render(request, 'ustsa_race_manager/races.html',{'past_races': past_races})


def athletes(request):
    all_athletes = Racer.objects.all()
    return render(request, 'ustsa_race_manager/athletes.html', {'all_athletes': all_athletes})


def athlete_detail(request, athlete_id):
    athlete = Racer.objects.get(id=athlete_id)
    athlete_results = RacerResult.objects.filter(racer=athlete.id)
    return render(request, 'ustsa_race_manager/athlete_detail.html', {'athlete': athlete, 'athlete_results': athlete_results})


