# Stdlib imports
from enum import Enum
from datetime import timedelta

# Core Django imports
from django.db import models
from django.urls import reverse


# Third-party app imports

# Imports from your apps
# from .managers import *

# Create your models here.

class Gender(Enum):
    M = 'Male'
    F = 'Female'

    @property
    def glongname(self):
        if self is Gender.M:
            return 'Mens'
        if self is Gender.F:
            return 'Ladies'

    @property
    def ilongname(self):
        if self is Gender.M:
            return 'Male'
        if self is Gender.F:
            return 'Female'

    @property
    def shortname(self):
        if self is Gender.M:
            return 'M'
        if self is Gender.F:
            return 'L'


class RacePointsManager(models.Manager):
    def set_race_points(self, race_id):
        race = Race.objects.get(id=race_id)
        best_time = race.racerresult_set.order_by('total_time').first().total_time
        for result in race.racerresult_set.all():
            result.calculate_race_points(best_time)

    def set_race_penalty(self, race_id):
        print("set_race_penalty called")
        class Result():
            def __init__(self, ustsa_points, race_points):
                self.ustsa_points = ustsa_points
                self.race_points = race_points

        points = []

        race = Race.objects.get(id=race_id)

        race_results = race.racerresult_set.all()

        for result in race_results:
            points.append(
                Result(
                    result.racer.racerpoints_set.get(current_valid_list=True, race_type='SP').ustsa_points,
                    result.race_points
               )
            )

        # Sort results by USTSA points to identify lowest 5 at start
        points.sort(key=lambda x: x.ustsa_points)
        a = sum(res.ustsa_points for res in points[:5])

        # Sort results by race points to find best 10
        points.sort(key=lambda x: x.race_points)
        del points[11:]

        # Sort best 10 results by USTSA points to find lowest 5 of top 10 finishers
        points.sort(key=lambda x: x.ustsa_points)
        b = sum(res.ustsa_points for res in points[:5])

        # Sum the race points of lowest 5 ustsa points of top 10 finishers
        c = sum(res.race_points for res in points[:5])

        # Apply the standard USATSA penalty formula
        penalty = (a + b - c) / 10

        # Store the applied penalty on the race model
        race.set_applied_penalty(penalty)

        for result in race_results:
            result.set_race_result(penalty)


class RaceOfficial(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    ussa_number = models.CharField(max_length=200)
    fis_td_number = models.CharField(max_length=200)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'


class Racer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    ustsa_num = models.CharField(max_length=200)
    inj = models.BooleanField()
    racer_gender = models.CharField(
        max_length=6,
        default='NG',
        choices=(
            (tag.name, tag.value) for tag in Gender
        ),
    )

    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


class Race(models.Model):
    STATUS_CHOICES = [
        ('i', 'Imported'),
        ('p', 'Published'),
    ]

    RACE_TYPES = (
        ('SP', 'Sprint Classic'),
        ('CL', 'Classic'),
        ('PS', 'Parallel Sprint'),
        ('GS', 'Giant Slalom')
    )

    STATE_CHOICES = (
        ('AL', 'Alabama'), ('AK', 'Alaska'), ('AS', 'American Samoa'), ('AZ', 'Arizona'), ('AR', 'Arkansas'),
        ('AA', 'Armed Forces Americas'), ('AE', 'Armed Forces Europe'), ('AP', 'Armed Forces Pacific'),
        ('CA', 'California'), ('CO', 'Colorado'), ('CT', 'Connecticut'), ('DE', 'Delaware'),
        ('DC', 'District of Columbia'),
        ('FL', 'Florida'), ('GA', 'Georgia'), ('GU', 'Guam'), ('HI', 'Hawaii'), ('ID', 'Idaho'), ('IL', 'Illinois'),
        ('IN', 'Indiana'), ('IA', 'Iowa'), ('KS', 'Kansas'), ('KY', 'Kentucky'), ('LA', 'Louisiana'), ('ME', 'Maine'),
        ('MD', 'Maryland'), ('MA', 'Massachusetts'), ('MI', 'Michigan'), ('MN', 'Minnesota'), ('MS', 'Mississippi'),
        ('MO', 'Missouri'), ('MT', 'Montana'), ('NE', 'Nebraska'), ('NV', 'Nevada'), ('NH', 'New Hampshire'),
        ('NJ', 'New Jersey'), ('NM', 'New Mexico'), ('NY', 'New York'), ('NC', 'North Carolina'),
        ('ND', 'North Dakota'),
        ('MP', 'Northern Mariana Islands'), ('OH', 'Ohio'), ('OK', 'Oklahoma'), ('OR', 'Oregon'),
        ('PA', 'Pennsylvania'),
        ('PR', 'Puerto Rico'), ('RI', 'Rhode Island'), ('SC', 'South Carolina'), ('SD', 'South Dakota'),
        ('TN', 'Tennessee'), ('TX', 'Texas'), ('UT', 'Utah'), ('VT', 'Vermont'), ('VI', 'Virgin Islands'),
        ('VA', 'Virginia'), ('WA', 'Washington'), ('WV', 'West Virginia'), ('WI', 'Wisconsin'), ('WY', 'Wyoming')
    )

    race_type = models.CharField(
        max_length=2,
        default='SP',
        choices=RACE_TYPES
    )

    race_name = models.CharField(
        max_length=200
    )

    race_date = models.DateField(
        verbose_name='Race Date'
    )

    location = models.CharField(
        max_length=200
    )

    state = models.CharField(
        max_length=200,
        choices=STATE_CHOICES
    )

    homoligation = models.CharField(
        max_length=200,
        default=0
    )

    officials = models.ManyToManyField(
        RaceOfficial,
        through='Assignments'
    )

    racers = models.ManyToManyField(
        Racer,
        through='RacerResult'
    )

    status = models.CharField(
        max_length=200,
        default='i',
        choices=STATUS_CHOICES
    )

    applied_penalty = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )

    objects = models.Manager()

    race_points = RacePointsManager()

    def set_applied_penalty(self, penalty, *args, **kwargs):
        self.applied_penalty = penalty
        super().save(*args, **kwargs)

    def __str__(self):
        return self.race_name

    def save(self, *args, **kwargs):
        self.season_code = self.race_date.year
        super().save(*args, **kwargs)


class Assignments(models.Model):
    POSITIONS = (
        ('ChiefRace', 'Chief of Race'),
        ('Datamanager', 'Data Manager'),
        ('Raceadmin', 'Race Administrator'),
        ('ChiefTiming', 'Chief of Timing'),
        ('Referee', 'Referee'),
        ('CourseChief', 'Course Chief'),
        ('StartReferee', 'Start Referee'),
        ('FinishReferee', 'Finish Referee'),
        ('TD', 'Technical Delegate'),
    )

    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE
    )

    race_official = models.ForeignKey(
        RaceOfficial,
        on_delete=models.CASCADE
    )

    position = models.CharField(
        max_length=20,
        choices=POSITIONS
    )

    def __str__(self):
        return f'{self.race.race_name}, {self.position}'


class RacerResult(models.Model):
    FINISH_TYPES = (
        ('CLR', 'Clear'),
        ('DNF', 'Did Not Finish'),
        ('DSQ', 'Disqualified'),
        ('DNS', 'Did Not Start')
    )
    JUMP_PENALTIES = [
        (timedelta(seconds=0.00), '0'),
        (timedelta(seconds=1.00), '1'),
        (timedelta(seconds=3.00), '3'),
        (timedelta(seconds=4.00), '4')
    ]

    bib = models.PositiveIntegerField(
        default=0
    )

    position = models.PositiveIntegerField(
        default=0
    )

    racer = models.ForeignKey(
        Racer,
        on_delete=models.CASCADE
    )

    race = models.ForeignKey(
        Race,
        on_delete=models.CASCADE
    )

    finish_type = models.CharField(
        max_length=3,
        default='CLR',
        choices=FINISH_TYPES
    )

    run_one_time = models.DurationField(
        default=timedelta(seconds=0)
    )

    run_one_gate_penalties = models.DurationField(
        default=timedelta(seconds=0)
    )

    run_one_jump_penalties = models.DurationField(
        choices=JUMP_PENALTIES,
        default=timedelta(seconds=0)
    )

    run_two_time = models.DurationField(
        default=timedelta(seconds=0)
    )

    run_two_gate_penalties = models.DurationField(
        default=timedelta(seconds=0)
    )

    run_two_jump_penalties = models.DurationField(
        choices=JUMP_PENALTIES,
        default=timedelta(seconds=0)
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['racer', 'race'], name='unique_race_result')
        ]

    total_time = models.DurationField(
        default=timedelta(seconds=0)
    )

    race_points = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )

    race_result = models.DecimalField(
        max_digits=10,
        decimal_places=3
    )

    def set_race_result(self, penalty, *args, **kwargs):
        self.race_result = self.race_points + penalty
        super().save(*args, **kwargs)

    def calculate_race_points(self, best_time, *args, **kwargs):
        self.race_points = (((self.total_time / best_time) - 1) * 500)
        super().save(*args, **kwargs)

    def calculate_total_time(self):
        self.total_time = self.run_one_time + self.run_one_gate_penalties + self.run_one_jump_penalties + self.run_two_time + self.run_two_gate_penalties + self.run_two_jump_penalties

    def save(self, *args, **kwargs):
        if self.total_time == timedelta(seconds=0):
            self.total_time = self.calculate_total_time()

        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.racer.first_name}, {self.race.race_name}'


class PublishedPointsList(models.Model):
    list_name = models.CharField(
        max_length=500
    )

    season_code = models.PositiveIntegerField()

    season_list_number = models.PositiveIntegerField()

    start_race_date = models.DateField()

    end_race_date = models.DateField()

    valid_from = models.DateField()

    valid_to = models.DateField()

    published = models.BooleanField()

    last_update = models.DateTimeField(
        auto_now=True
    )

    objects = models.Manager()

    def create_points_list(self):
        RacerResult.objects.get(date__range=["2011-01-01", "2011-01-31"])

    def save(self, *args, **kwargs):
        self.create_points_list()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.list_name


class RacerPoints(models.Model):
    RACE_TYPES = (
        ('SP', 'Sprint Classic'),
        ('CL', 'Classic'),
        ('PS', 'Parallel Sprint'),
        ('GS', 'Giant Slalom')
    )

    PENALTY_TYPES = (
        ('+', 'Single Event Result'),
        ('*', 'No Results Since Base Season List'),
        ('>', 'No Results During Last Year'),
        (None, 'No Penalty Applied')
    )

    list_id = models.ForeignKey(
        PublishedPointsList,
        on_delete=models.CASCADE
    )

    racer = models.ForeignKey(
        Racer,
        on_delete=models.CASCADE
    )

    race_type = models.CharField(
        max_length=2,
        default='SP',
        choices=RACE_TYPES
    )

    ustsa_points = models.DecimalField(
        max_digits=7,
        decimal_places=3,
        default=500.000
    )

    position = models.PositiveIntegerField()

    penalty = models.CharField(
        max_length=2,
        default='',
        choices=PENALTY_TYPES
    )

    current_valid_list = models.BooleanField(
        default=False
    )

    list_published = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f'{self.racer.first_name}, {self.racer.last_name}: {self.list_id.list_name}'

# class BestRace(models.Model):
#     race = models.ForeignKey(
#         Race,
#         on_delete=models.CASCADE
#     )
#
#     racer = models.ForeignKey(
#         Racer,
#         on_delete=models.CASCADE
#     )
#
#
# class SecondRace(models.Model):
#     race = models.ForeignKey(
#         Race,
#         on_delete=models.CASCADE
#     )
#
#     racer = models.ForeignKey(
#         Racer,
#         on_delete=models.CASCADE
#     )
