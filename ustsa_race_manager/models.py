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
    RACE_TYPES = (
        ('SP', 'Sprint Classic'),
        ('CL', 'Classic'),
        ('PS', 'Parallel Sprint'),
        ('GS', 'Giant Slalom')
    )

    race_type = models.CharField(
        max_length=2,
        default='SP',
        choices=RACE_TYPES
    )
    race_name = models.CharField(max_length=200)
    race_date = models.DateField(verbose_name='Race Date')
    location = models.CharField(max_length=200)
    homoligation = models.CharField(max_length=200, default=0)
    officials = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.race_name


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
    
    def __str__(self):
        return f'{self.last_name}, {self.first_name}'


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
        default=timedelta(minutes=40)
    )

    run_one_gate_penalties = models.DurationField(
        default=timedelta(seconds=0)
    )
    
    run_one_jump_penalties = models.DurationField(
        choices=JUMP_PENALTIES,
        default=timedelta(seconds=0)
    )
    
    run_two_time = models.DurationField(
        default=timedelta(minutes=40)
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
    
    def calculate_total_time (self):
        total_time = self.run_one_time + self.run_one_gate_penalties + self.run_one_jump_penalties + self.run_two_time + self.run_two_gate_penalties + self.run_two_jump_penalties
        return total_time
    
    def save(self, *args, **kwargs):
        self.total_time = self.calculate_total_time()
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.racer.first_name}, {self.race.race_name}'
