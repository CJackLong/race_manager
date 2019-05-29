# Stdlib imports
from enum import Enum
from datetime import timedelta

# Core Django imports
from django.db import models
from django.urls import reverse

# Third-party app imports

# Imports from your apps


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


class Race(models.Model):
    race_name = models.CharField(max_length=200)
    race_date = models.DateField(verbose_name='Race Date')
    location = models.CharField(max_length=200)
    homoligation = models.CharField(max_length=200, default=0)
    officials = models.CharField(max_length=200, null=True)

    @property
    def __str__(self):
        return self.race_name

    @property
    def get_absolute_url(self):
        return reverse('race_detail', args=[str(self.id)])


class Racer(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    ustsa_num = models.CharField(max_length=200)
    inj = models.CharField(max_length=200)
    racer_gender = models.CharField(
        max_length=6,
        default='NG',
        choices=(
            (tag.name, tag.value) for tag in Gender
        ),
    )

    @property
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'

    @property
    def get_absolute_url(self):
        return reverse('athlete_detail', args=[str(self.id)])


class RacerResult(models.Model):
    FINISH_TYPES = (
        ('CLR', 'Clear'),
        ('DNF', 'Did Not Finish'),
        ('DSQ', 'Disqualified'),
        ('DNS', 'Did Not Start')
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

    race_time = models.DurationField(
        default=timedelta(minutes=40)
    )

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['racer', 'race'], name='unique_race_result')
    ]

    @property
    def __str__(self):
        return f'{self.racer.first_name}, {self.race.race_name}'
