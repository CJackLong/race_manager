# Generated by Django 2.2 on 2019-06-06 05:45

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ustsa_race_manager', '0008_racerresult_total_time'),
    ]

    operations = [
        migrations.AddField(
            model_name='race',
            name='racers',
            field=models.ManyToManyField(through='ustsa_race_manager.RacerResult', to='ustsa_race_manager.Racer'),
        ),
        migrations.AlterField(
            model_name='racer',
            name='inj',
            field=models.BooleanField(),
        ),
        migrations.AlterField(
            model_name='racerresult',
            name='run_one_time',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
        migrations.AlterField(
            model_name='racerresult',
            name='run_two_time',
            field=models.DurationField(default=datetime.timedelta(0)),
        ),
    ]