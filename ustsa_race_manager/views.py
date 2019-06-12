from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.db.models import Sum

from .models import Race, Racer, RacerResult

# Create your views here.
def calendar(request):

    num_races = Race.objects.filter(status='p').count()
    num_racers = Racer.objects.all().count()
    recent_races = Race.objects.order_by('race_date')

    context = {
        'recent_races': recent_races,
        'num_races':num_races,
        'num_racers': num_racers
    }

    return render(request, 'ustsa_race_manager/calendar.html', context)


def race_detail(request, race_name):
    race = get_object_or_404(Race, race_name=race_name)

    officials = race.assignments_set.all()

    for official in officials:
        print(official.race_official, official.position)

    race_results = RacerResult.objects.filter(race=race.id).order_by('total_time')

    #for e in race_results:
    #    print(str(e.total_time))

    return render(
        request,
        'ustsa_race_manager/race_detail.html',
        {
            'race': race,
            'race_results': race_results,
            'officials': officials
        }
    )


def races(request):
    past_races = Race.objects.filter(status='p')
    return render(request, 'ustsa_race_manager/races.html',{'past_races': past_races})


def athletes(request):
    all_athletes = Racer.objects.all()
    return render(request, 'ustsa_race_manager/athletes.html', {'all_athletes': all_athletes})


def athlete_detail(request, ustsa_num):
    athlete = Racer.objects.get(ustsa_num=ustsa_num)
    athlete_results = RacerResult.objects.filter(racer=athlete.id)
    return render(request, 'ustsa_race_manager/athlete_detail.html', {'athlete': athlete, 'athlete_results': athlete_results})


